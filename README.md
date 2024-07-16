# CloudFormation Templates & Python Automations

Bem-vindo ao repositório de Templates CloudFormation e Automações em Python. Este repositório contém uma coleção de templates de infraestrutura como código (IaC) utilizando AWS CloudFormation, além de scripts de automação desenvolvidos em Python para diversas tarefas relacionadas à operação e manutenção de infraestrutura em nuvem.

## Índice

- [Visão Geral](#visão-geral)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)

## Visão Geral

Este repositório foi criado para facilitar a gestão e a automação de infraestrutura na AWS. Os templates de CloudFormation permitem a criação e a configuração de recursos de forma declarativa e reproduzível. As automações em Python complementam essa abordagem, fornecendo scripts para tarefas comuns de administração, monitoramento e manutenção.

## Requisitos

- **AWS CLI**: Para interação com os serviços da AWS.
- **Python 3.8+**: Para execução dos scripts de automação.
- **Boto3**: Biblioteca AWS SDK para Python.

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Instale as dependências Python:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### CloudFormation

Para criar uma pilha CloudFormation usando um dos templates, use o seguinte comando:
```sh
aws cloudformation create-stack --stack-name minha-pilha --template-body file://caminho/para/o/template.yml