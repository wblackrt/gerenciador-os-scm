"""Gerenciador acadêmico de ordens de serviço; dados de demonstração fictícios."""
import argparse
import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).resolve().parent / "dados" / "ordens.json"
STATUS_PERMITIDOS = {"Aberta", "Em andamento", "Concluida"}


def carregar_ordens(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    conteudo = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(conteudo, list):
        raise ValueError("A base de ordens deve conter uma lista JSON.")
    return conteudo


def salvar_ordens(ordens, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(ordens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def criar_os(cliente, equipamento, defeito, caminho=ARQUIVO_PADRAO):
    if not all(isinstance(item, str) and item.strip() for item in (cliente, equipamento, defeito)):
        raise ValueError("Cliente, equipamento e defeito são obrigatórios.")
    ordens = carregar_ordens(caminho)
    novo_id = max((ordem["id"] for ordem in ordens), default=0) + 1
    nova = {"id": novo_id, "cliente": cliente.strip(), "equipamento": equipamento.strip(),
            "defeito": defeito.strip(), "status": "Aberta"}
    ordens.append(nova)
    salvar_ordens(ordens, caminho)
    return nova


def atualizar_status(identificador, novo_status, caminho=ARQUIVO_PADRAO):
    if novo_status not in STATUS_PERMITIDOS:
        raise ValueError(f"Status inválido: {novo_status}")
    ordens = carregar_ordens(caminho)
    for ordem in ordens:
        if ordem["id"] == identificador:
            ordem["status"] = novo_status
            salvar_ordens(ordens, caminho)
            return ordem
    raise ValueError(f"OS #{identificador} não encontrada.")


def resumo(ordens):
    return {status: sum(o["status"] == status for o in ordens) for status in sorted(STATUS_PERMITIDOS)}


def main():
    parser = argparse.ArgumentParser(description="Gerenciador acadêmico de ordens de serviço")
    sub = parser.add_subparsers(dest="acao", required=True)
    sub.add_parser("listar", help="Exibir as ordens")
    novo = sub.add_parser("nova", help="Cadastrar OS")
    novo.add_argument("cliente")
    novo.add_argument("equipamento")
    novo.add_argument("defeito")
    conclui = sub.add_parser("concluir", help="Concluir OS")
    conclui.add_argument("id", type=int)
    sub.add_parser("resumo", help="Exibir totais por status")
    args = parser.parse_args()
    try:
        if args.acao == "nova":
            ordem = criar_os(args.cliente, args.equipamento, args.defeito)
            print(f"OS #{ordem['id']} cadastrada com sucesso.")
        elif args.acao == "concluir":
            ordem = atualizar_status(args.id, "Concluida")
            print(f"OS #{ordem['id']} concluída com sucesso.")
        elif args.acao == "listar":
            ordens = carregar_ordens()
            if not ordens:
                print("Nenhuma ordem de serviço cadastrada.")
            for ordem in ordens:
                print(f"OS #{ordem['id']:03d} | {ordem['cliente']} | {ordem['equipamento']} | {ordem['status']}")
        elif args.acao == "resumo":
            for status, quantidade in resumo(carregar_ordens()).items():
                print(f"{status}: {quantidade}")
    except (ValueError, json.JSONDecodeError) as erro:
        parser.exit(2, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
