from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET_KEY = 'admin20@25'

USER_DB = [
    {
        'user_id': 1,
        'name': 'Alberto Silva',
        'username': 'ASilva.counter',
        'password': '1234',
        'admin': False
    },
    {
        'user_id': 2,
        'name': 'Fátima Almeida',
        'username': 'FAlmeida.manager',
        'password': '4321',
        'admin': True
    }
]


products = [
    {"id": 1, "product_name": "Coleira", "product_description": "Coleira para cachorro de pequeno porte", "product_price": 23.90, "product_photo": "", "stock_quantity": 26},
    {"id": 2, "product_name": "Ração para cães adultos", "product_description": "Ração premium para cães adultos de médio porte", "product_price": 119.90, "product_photo": "", "stock_quantity": 40},
    {"id": 3, "product_name": "Areia para gatos", "product_description": "Areia higiênica com controle de odor para gatos", "product_price": 35.00, "product_photo": "", "stock_quantity": 60},
    {"id": 4, "product_name": "Brinquedo de borracha", "product_description": "Brinquedo mordedor em formato de osso", "product_price": 15.00, "product_photo": "", "stock_quantity": 75},
    {"id": 5, "product_name": "Comedouro duplo", "product_description": "Comedouro e bebedouro acoplado para cães e gatos", "product_price": 29.90, "product_photo": "", "stock_quantity": 30},
    {"id": 6, "product_name": "Tapete higiênico", "product_description": "Tapete absorvente para cães", "product_price": 39.90, "product_photo": "", "stock_quantity": 45},
    {"id": 7, "product_name": "Shampoo para cães", "product_description": "Shampoo neutro para cães com pele sensível", "product_price": 22.50, "product_photo": "", "stock_quantity": 50},
    {"id": 8, "product_name": "Antipulgas", "product_description": "Medicamento antipulgas em comprimido para cães", "product_price": 89.00, "product_photo": "", "stock_quantity": 20},
    {"id": 9, "product_name": "Caixa de transporte", "product_description": "Caixa de transporte tamanho médio", "product_price": 150.00, "product_photo": "", "stock_quantity": 12},
    {"id": 10, "product_name": "Osso de couro", "product_description": "Osso natural para mastigação", "product_price": 9.90, "product_photo": "", "stock_quantity": 80},
    {"id": 11, "product_name": "Cama para cachorro", "product_description": "Cama acolchoada tamanho G", "product_price": 120.00, "product_photo": "", "stock_quantity": 18},
    {"id": 12, "product_name": "Ração para gatos filhotes", "product_description": "Ração específica para crescimento saudável", "product_price": 92.00, "product_photo": "", "stock_quantity": 34},
    {"id": 13, "product_name": "Bebedouro automático", "product_description": "Fonte com filtro para cães e gatos", "product_price": 99.90, "product_photo": "", "stock_quantity": 22},
    {"id": 14, "product_name": "Escova de pelos", "product_description": "Escova com cerdas macias para remoção de pelos mortos", "product_price": 18.90, "product_photo": "", "stock_quantity": 55},
    {"id": 15, "product_name": "Brinquedo de pelúcia", "product_description": "Brinquedo com apito para cães", "product_price": 25.00, "product_photo": "", "stock_quantity": 48},
    {"id": 16, "product_name": "Coleira peitoral", "product_description": "Coleira tipo peitoral para cães médios", "product_price": 35.00, "product_photo": "", "stock_quantity": 27},
    {"id": 17, "product_name": "Ração para roedores", "product_description": "Alimento completo para hamster e porquinho da índia", "product_price": 19.90, "product_photo": "", "stock_quantity": 38},
    {"id": 18, "product_name": "Areia sílica para gatos", "product_description": "Areia higiênica de sílica com alta absorção", "product_price": 42.00, "product_photo": "", "stock_quantity": 32},
    {"id": 19, "product_name": "Pente para pulgas", "product_description": "Pente de aço para remoção de pulgas e ovos", "product_price": 14.90, "product_photo": "", "stock_quantity": 44},
    {"id": 20, "product_name": "Bolinha de tênis", "product_description": "Brinquedo resistente para cães", "product_price": 12.00, "product_photo": "", "stock_quantity": 70},
    {"id": 21, "product_name": "Ração para cães filhotes", "product_description": "Ração específica para cães em fase de crescimento", "product_price": 110.00, "product_photo": "", "stock_quantity": 37},
    {"id": 22, "product_name": "Coleira com plaquinha", "product_description": "Coleira com plaquinha de identificação gravável", "product_price": 28.50, "product_photo": "", "stock_quantity": 29},
    {"id": 23, "product_name": "Petisco dental", "product_description": "Snack para limpeza dos dentes", "product_price": 20.00, "product_photo": "", "stock_quantity": 65},
    {"id": 24, "product_name": "Toca para gatos", "product_description": "Toca de tecido para gatos dormirem confortavelmente", "product_price": 95.00, "product_photo": "", "stock_quantity": 16},
    {"id": 25, "product_name": "Roupinha para cachorro", "product_description": "Roupa de frio tamanho P", "product_price": 45.00, "product_photo": "", "stock_quantity": 35},
    {"id": 26, "product_name": "Limpador de patas", "product_description": "Copo com cerdas para lavar as patas dos cães", "product_price": 30.00, "product_photo": "", "stock_quantity": 28},
    {"id": 27, "product_name": "Tesoura para unhas", "product_description": "Tesoura especial para cortar unhas de pets", "product_price": 17.90, "product_photo": "", "stock_quantity": 50},
    {"id": 28, "product_name": "Coleira refletiva", "product_description": "Coleira com fita refletiva para segurança noturna", "product_price": 32.00, "product_photo": "", "stock_quantity": 23},
    {"id": 29, "product_name": "Ração úmida para gatos", "product_description": "Sachê com pedaços de carne em molho", "product_price": 4.90, "product_photo": "", "stock_quantity": 100},
    {"id": 30, "product_name": "Desinfetante pet", "product_description": "Desinfetante seguro para uso em ambientes com animais", "product_price": 24.90, "product_photo": "", "stock_quantity": 40},
    {"id": 31, "product_name": "Shampoo para gatos", "product_description": "Shampoo seco para higiene de gatos", "product_price": 27.00, "product_photo": "", "stock_quantity": 33},
    {"id": 32, "product_name": "Arranhador pequeno", "product_description": "Arranhador de papelão reciclável", "product_price": 59.00, "product_photo": "", "stock_quantity": 21},
    {"id": 33, "product_name": "Escova dental", "product_description": "Escova dupla para higiene bucal de cães e gatos", "product_price": 13.50, "product_photo": "", "stock_quantity": 46},
    {"id": 34, "product_name": "Mordedor com corda", "product_description": "Brinquedo resistente com corda para puxar", "product_price": 19.00, "product_photo": "", "stock_quantity": 36},
    {"id": 35, "product_name": "Porta petiscos", "product_description": "Brinquedo dispenser de petiscos", "product_price": 49.90, "product_photo": "", "stock_quantity": 27},
    {"id": 36, "product_name": "Fonte para gatos", "product_description": "Fonte elétrica com filtro para gatos beberem mais água", "product_price": 135.00, "product_photo": "", "stock_quantity": 14},
    {"id": 37, "product_name": "Casinha plástica", "product_description": "Casinha para cães pequenos", "product_price": 180.00, "product_photo": "", "stock_quantity": 10},
    {"id": 38, "product_name": "Spray educador", "product_description": "Spray para evitar xixi fora do lugar", "product_price": 34.90, "product_photo": "", "stock_quantity": 24},
    {"id": 39, "product_name": "Tapete gelado", "product_description": "Tapete refrescante para dias quentes", "product_price": 79.90, "product_photo": "", "stock_quantity": 19},
    {"id": 40, "product_name": "Luva removedora de pelos", "product_description": "Luva que remove pelos soltos durante o carinho", "product_price": 21.90, "product_photo": "", "stock_quantity": 42},
    {"id": 41, "product_name": "Bolsa para transporte", "product_description": "Bolsa acolchoada para gatos e cães de pequeno porte", "product_price": 99.00, "product_photo": "", "stock_quantity": 13},
    {"id": 42, "product_name": "Cinto de segurança", "product_description": "Cinto que prende o pet no carro com segurança", "product_price": 36.00, "product_photo": "", "stock_quantity": 25},
    {"id": 43, "product_name": "Colônia pet", "product_description": "Colônia com fragrância suave para pets", "product_price": 26.00, "product_photo": "", "stock_quantity": 30},
    {"id": 44, "product_name": "Cortador elétrico de pelos", "product_description": "Máquina para tosa caseira de cães e gatos", "product_price": 199.00, "product_photo": "", "stock_quantity": 9},
    {"id": 45, "product_name": "Brinquedo interativo", "product_description": "Jogo de inteligência para cães e gatos", "product_price": 89.00, "product_photo": "", "stock_quantity": 18},
    {"id": 46, "product_name": "Guia retrátil", "product_description": "Guia extensível para passeios", "product_price": 59.90, "product_photo": "", "stock_quantity": 31},
    {"id": 47, "product_name": "Ração para peixe beta", "product_description": "Ração específica para peixes ornamentais", "product_price": 8.90, "product_photo": "", "stock_quantity": 50},
    {"id": 48, "product_name": "Termômetro aquático", "product_description": "Termômetro para controle da temperatura em aquários", "product_price": 12.00, "product_photo": "", "stock_quantity": 20},
    {"id": 49, "product_name": "Filtro para aquário", "product_description": "Filtro de carvão ativado para aquários", "product_price": 45.00, "product_photo": "", "stock_quantity": 15},
    {"id": 50, "product_name": "Luz UV para aquário", "product_description": "Iluminação e esterilização para aquários", "product_price": 72.00, "product_photo": "", "stock_quantity": 11},
]


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False


@app.route('/products', methods=['GET'])
def get_products():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify(message="Token é necessário!"), 403

    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify(message="Cabeçalho de autorização malformado!"), 401

    if not verify_token(parts[1]):
        return jsonify(message="Token inválido ou expirado!"), 403

    preco_asc = request.args.get('preco_asc', '').lower() == 'true'
    preco_desc = request.args.get('preco_desc', '').lower() == 'true'
    description_part = request.args.get('description_part', '').lower()

    if description_part:
        produtos_filtrados = [produto for produto in products if
                              description_part in produto['product_description'].lower()]
        return jsonify(produtos_filtrados)
    elif preco_asc:
        produtos_ordenados = sorted(products, key=lambda x: x['product_price'])
        return jsonify(produtos_ordenados)
    elif preco_desc:
        produtos_ordenados = sorted(products, key=lambda x: x['product_price'], reverse=True)
        return jsonify(produtos_ordenados)
    else:
        return jsonify(products)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify(message="Token é necessário!"), 403

    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify(message="Cabeçalho de autorização malformado!"), 401

    if not verify_token(parts[1]):
        return jsonify(message="Token inválido ou expirado!"), 403

    produto = next((p for p in products if p['id'] == product_id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"message": "Produto não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)