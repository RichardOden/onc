"""Command-line interface for ONC.

    onc list-genes            show the active gene pool
    onc run [--gene SYMBOL]   run one gene (default: a full pass over the pool)
    onc chain verify PATH     verify a saved hash chain
    onc version               print the ONC version

Runs fully offline against the bundled fixture, so `onc run` works with no
network access or API keys.
"""

from __future__ import annotations

import argparse
import sys

from onc import __version__
from onc.genes import pool
from onc.hashchain import HashChain
from onc.pipeline import run_experiment, run_pass


def _cmd_list_genes(_: argparse.Namespace) -> int:
    for g in pool():
        print(f"  {g.symbol:12s}  {g.cancer:28s}  {g.rationale}")
    return 0


def _print_experiment(exp) -> None:
    sc = exp.scorecard
    mark = "PASS" if exp.passed else "FAIL"
    flag = "CONFIRMED" if sc.confirmed else "rejected"
    print(
        f"  {sc.symbol:10s} weighted={sc.weighted:.2f} dep={sc.dependency:.2f}"
        f"  {flag:9s}  verify={mark}  hash={exp.receipt.hash[:10]}"
    )


def _cmd_run(args: argparse.Namespace) -> int:
    chain = HashChain()
    if args.gene:
        exp = run_experiment(args.gene, chain)
        _print_experiment(exp)
    else:
        results = run_pass(chain)
        for exp in results:
            _print_experiment(exp)
        confirmed = sum(1 for e in results if e.scorecard.confirmed)
        passed = sum(1 for e in results if e.passed)
        print(
            f"\n  {len(results)} genes · {confirmed} confirmed · "
            f"{passed}/{len(results)} verified · chain intact: {chain.verify()}"
        )
    if args.out:
        chain.save(args.out)
        print(f"  chain written to {args.out}")
    return 0


def _cmd_chain_verify(args: argparse.Namespace) -> int:
    chain = HashChain.load(args.path)
    ok = chain.verify()
    print(f"  {len(chain)} receipts · chain intact: {ok}")
    return 0 if ok else 1


def _cmd_version(_: argparse.Namespace) -> int:
    print(f"onc {__version__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="onc", description="autonomous pediatric cancer gene-dependency scientist")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("list-genes", help="show the active gene pool").set_defaults(func=_cmd_list_genes)

    run = sub.add_parser("run", help="run the pipeline")
    run.add_argument("--gene", help="run a single gene by symbol")
    run.add_argument("--out", help="write the resulting hash chain to this path")
    run.set_defaults(func=_cmd_run)

    chain = sub.add_parser("chain", help="hash-chain operations")
    chain_sub = chain.add_subparsers(dest="chain_command", required=True)
    cv = chain_sub.add_parser("verify", help="verify a saved chain")
    cv.add_argument("path")
    cv.set_defaults(func=_cmd_chain_verify)

    sub.add_parser("version", help="print version").set_defaults(func=_cmd_version)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
