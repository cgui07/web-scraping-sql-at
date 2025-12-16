import csv
import requests
from bs4 import BeautifulSoup

URL = "https://pedrovncs.github.io/lindosprecos/produtos.html"
CSV_DESTINO = "dados/produtos.csv"

def gerar_produtos_csv():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    produtos = soup.select(".product-card")

    if not produtos:
        raise RuntimeError("Nenhum produto encontrado no site")

    with open(CSV_DESTINO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_produto", "nome", "quantidade", "preco"])

        for idx, produto in enumerate(produtos, start=1):
            nome = produto.select_one(".card-title").get_text(strip=True)

            preco_raw = produto.select_one(".card-price").get_text()
            preco = (
                preco_raw.replace("Valor:", "")
                .replace("R$", "")
                .replace("\xa0", "")
                .replace(",", ".")
                .strip()
            )

            qtd_text = produto.select_one("p[data-qtd]").get_text()
            quantidade = int("".join(filter(str.isdigit, qtd_text)))

            writer.writerow([idx, nome, quantidade, float(preco)])

    print(f"CSV gerado com sucesso em {CSV_DESTINO}")
if __name__ == "__main__":
    gerar_produtos_csv()