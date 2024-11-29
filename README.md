# fastapi-crud-mysql-to-ecr

🎑🎑🎑 簡単なFastAPIアプリケーション(DB/MySQLのCRUD操作あり)をECRにデプロイしてみる！  

## ECRをプルして利用するために必要な事項

ECRにプッシュされた当イメージを使用するためには、以下の環境変数が必要です。  

| 環境変数名 | 説明 |
| --- | --- |
| DB_HOST | DBのホスト |
| DB_PORT | DBのポート |
| DB_USERNAME | DBのユーザー名 |
| DB_PASSWORD | DBのパスワード |
| DB_DATABASE | DBのデータベース名 |

また、`./mysql_init/`ディレクトリ内のDDLのSQLが実行されることを前提としています。  

## ローカルでの開発

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

export ECR_REPOSITORY_URI=$(aws ecr describe-repositories --repository-names fastapi-crud-app --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}

docker build -t fastapi-crud-app ./fastapi-app/
docker tag fastapi-crud-app:latest ${ECR_REPOSITORY_URI}:latest
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

---

デプロイされたECRをローカルでテストする場合には、以下のコマンドを実行してください。  

```shell
docker compose down
docker compose up -d db

export ECR_REPOSITORY_URI=$(aws ecr describe-repositories --repository-names fastapi-crud-app --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}

docker run --rm -p 80:80 --name fastapi-crud-app -e DB_HOST=$(ipconfig getifaddr en0) -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=rootpassword ${ECR_REPOSITORY_URI}:latest
```
