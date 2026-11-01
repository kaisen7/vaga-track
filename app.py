"""Organizador de candidaturas. Execute python app.py --help."""
import argparse
import csv
import sqlite3
from datetime import date
from pathlib import Path

STATUS = ('enviada', 'entrevista', 'aprovada', 'encerrada')

def conectar(caminho):
    db = sqlite3.connect(caminho)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY, empresa TEXT NOT NULL, cargo TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'enviada', criada TEXT NOT NULL)""")
    return db

def adicionar(db, empresa, cargo):
    empresa, cargo = empresa.strip(), cargo.strip()
    if not empresa or not cargo:
        raise ValueError('Empresa e cargo não podem ficar vazios.')
    with db:
        cursor = db.execute('INSERT INTO vagas(empresa,cargo,criada) VALUES(?,?,?)',
                            (empresa, cargo, date.today().isoformat()))
    return cursor.lastrowid

def atualizar(db, numero, status):
    if status not in STATUS:
        raise ValueError('Status inválido.')
    with db:
        result = db.execute('UPDATE vagas SET status=? WHERE id=?', (status, numero))
    if result.rowcount == 0:
        raise ValueError('Candidatura não encontrada.')

def listar(db, status=None):
    if status:
        return db.execute('SELECT * FROM vagas WHERE status=? ORDER BY id DESC', (status,)).fetchall()
    return db.execute('SELECT * FROM vagas ORDER BY id DESC').fetchall()

def main():
    parser = argparse.ArgumentParser(description='Organize seu processo de busca por estágio.')
    parser.add_argument('--banco', default=str(Path(__file__).with_name('vagas.db')))
    commands = parser.add_subparsers(dest='comando', required=True)
    add = commands.add_parser('adicionar')
    add.add_argument('empresa'); add.add_argument('cargo')
    ls = commands.add_parser('listar'); ls.add_argument('--status', choices=STATUS)
    change = commands.add_parser('atualizar')
    change.add_argument('id', type=int); change.add_argument('status', choices=STATUS)
    commands.add_parser('resumo')
    export = commands.add_parser('exportar'); export.add_argument('arquivo')
    args = parser.parse_args()
    db = conectar(args.banco)
    try:
        if args.comando == 'adicionar':
            print('Candidatura cadastrada:', adicionar(db, args.empresa, args.cargo))
        elif args.comando == 'atualizar':
            atualizar(db, args.id, args.status); print('Status atualizado.')
        elif args.comando == 'listar':
            rows = listar(db, args.status)
            if not rows: print('Nenhuma candidatura encontrada.')
            for row in rows:
                print(f"#{row['id']} | {row['empresa']} | {row['cargo']} | {row['status']} | {row['criada']}")
        elif args.comando == 'resumo':
            rows = listar(db)
            print(f'Total: {len(rows)}')
            for status in STATUS:
                print(f'{status}: {sum(row["status"] == status for row in rows)}')
        elif args.comando == 'exportar':
            with open(args.arquivo, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'empresa', 'cargo', 'status', 'criada'])
                for row in listar(db):
                    # Evita fórmulas ao abrir textos em aplicativos de planilha.
                    writer.writerow([("'" + v if isinstance(v,str) and v.startswith(('=', '+', '-', '@')) else v) for v in row])
            print('CSV exportado.')
    except (ValueError, OSError) as error:
        parser.exit(1, f'Erro: {error}\n')
    finally:
        db.close()

if __name__ == '__main__':
    main()
