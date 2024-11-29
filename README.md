# fastapi-crud-mysql-to-ecr

🎑🎑🎑 簡単なFastAPIアプリケーション(DB/MySQLのCRUD操作あり)をECRにデプロイしてみる！  

[![ci](https://github.com/osawa-koki/fastapi-crud-mysql-to-ecr/actions/workflows/ci.yml/badge.svg)](https://github.com/osawa-koki/fastapi-crud-mysql-to-ecr/actions/workflows/ci.yml)
[![cd](https://github.com/osawa-koki/fastapi-crud-mysql-to-ecr/actions/workflows/cd.yml/badge.svg)](https://github.com/osawa-koki/fastapi-crud-mysql-to-ecr/actions/workflows/cd.yml)
[![Dependabot Updates](https://github.com/osawa-koki/fastapi-crud-mysql-to-ecr/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/osawa-koki/fastapi-crud-mysql-to-ecr/actions/workflows/dependabot/dependabot-updates)

![成果物](./fruit.gif)  

## ECRをプルして利用するために必要な事項

ECRにプッシュされた当イメージを使用するためには、以下の環境変数が必要です。  

| 環境変数名 | 説明 |
| --- | --- |
| DB_HOST | DBのホスト |
| DB_PORT | DBのポート |
| DB_USERNAME | DBのユーザー名 |
| DB_PASSWORD | DBのパスワード |
| DB_DATABASE | DBのデータベース名 |

また、`./mysql_init/`ディレクトリ内のSQLが実行されていることを前提としています。  

## ローカルでの開発

`.env.example`をコピーして、`.env`を作成してください。  
中身を適切に設定してください。  

以下のコマンドを実行してください。  

```shell
docker compose build
docker compose up -d
```

コンテナ内でPythonでの開発を行う場合には、以下のコマンドを実行してください。  

```shell
cd ./fastapi-app/

apt update
apt install python3.11-venv

python -m venv /myenv/
source /myenv/bin/activate
pip install -r ./requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 80
```

## デプロイ

DevContainerに入り、以下のコマンドを実行してください。  
※ `~/.aws/credentials`にAWSの認証情報があることを前提とします。  

```shell
cdk deploy

source .env

export ECR_REPOSITORY_URI=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}

docker build -t ${ECR_REPOSITORY_NAME} ./fastapi-app/
docker tag ${ECR_REPOSITORY_NAME}:latest ${ECR_REPOSITORY_URI}:latest
docker push ${ECR_REPOSITORY_URI}:latest
```

GitHub Actionsでデプロイする場合には、以下のシークレットを設定してください。  

| シークレット名 | 説明 |
| --- | --- |
| AWS_ACCESS_KEY_ID | AWSのアクセスキーID |
| AWS_SECRET_ACCESS_KEY | AWSのシークレットアクセスキー |
| AWS_REGION | AWSのリージョン |

タグをプッシュすると、GitHub Actionsがデプロイを行います。  
手動でトリガーすることも可能です。  

## デプロイ後の動作確認

デプロイされたECRをローカルでテストする場合には、以下のコマンドを実行してください。  
※ このコマンドはローカルで実行してください。  

```shell
docker compose down
docker compose up -d db

source .env

export ECR_REPOSITORY_URI=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}

docker run --rm -p 80:80 --name ${ECR_REPOSITORY_NAME} \
  -e DB_HOST=$(ipconfig getifaddr en0) \
  -e DB_PORT=3306 \
  -e DB_USERNAME=root \
  -e DB_PASSWORD=rootpassword \
  -e DB_DATABASE=mydb \
  ${ECR_REPOSITORY_URI}:latest
```
