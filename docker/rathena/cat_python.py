#!/usr/bin/env python3

import os
import argparse


def print_file(path):

    if not os.path.exists(path):
        print("Arquivo nao encontrado:", path)
        return

    print("\n" + "=" * 60)
    print(path)
    print("=" * 60)

    try:
        with open(path, "r", encoding="utf8", errors="ignore") as f:
            print(f.read())
    except Exception as e:
        print("Erro ao ler:", e)


def list_files(root):

    files = []

    for r, d, f in os.walk(root):
        for name in f:
            files.append(os.path.join(r, name))

    return sorted(files)


def confirm_scan(root):

    files = list_files(root)

    print("\nArquivos encontrados:", len(files))

    for f in files[:10]:
        print(" ", f)

    if len(files) > 10:
        print(" ...")

    ans = input("\nMostrar TODOS os arquivos? (y/N): ")

    if ans.lower() != "y":
        print("Abortado.")
        return

    for f in files:
        print_file(f)


def main():

    parser = argparse.ArgumentParser(description="Config cat scanner")

    parser.add_argument("-d", "--dir", help="diretorio root")
    parser.add_argument("-f", "--files", nargs="+", help="arquivos especificos")

    args = parser.parse_args()

    # caso 3
    if args.dir and args.files:

        for f in args.files:
            path = os.path.join(args.dir, f)
            print_file(path)

        return

    # caso 1
    if args.files and not args.dir:

        for f in args.files:
            print_file(f)

        return

    # caso 2
    if args.dir and not args.files:

        confirm_scan(args.dir)
        return

    # caso 4

    path = input("Digite a pasta para scan: ").strip()

    if not os.path.exists(path):
        print("Caminho invalido.")
        return

    confirm_scan(path)


if __name__ == "__main__":
    main()
