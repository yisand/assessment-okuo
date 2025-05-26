build-lambda:
	docker buildx build --platform linux/amd64 --provenance=false -t docker-image-lambda-transform:test .

test-lambda:
	docker run --env-file .env --platform linux/amd64 -p 9000:8080 docker-image-lambda-transform:test 

test-lambda-win:
	make test-lambda
	Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -Body '{}' -ContentType "application/json"

test-lambda-linux:
	make test-lambda
	curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

deploy-lambda:
	make build-lambda
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <reemplazar_con_AWS_account_id>.dkr.ecr.us-east-1.amazonaws.com
	aws ecr create-repository --repository-name lambda-transformacion-imagen --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
	docker tag docker-image-lambda-transform:test <ECRrepositoryUri_obtenido_del_comando_anterior>:latest
	docker push <reemplazar_con_AWS_account_id>.dkr.ecr.us-east-1.amazonaws.com/lambda-transformacion-imagen:latest
	aws lambda create-function \
		--function-name lambda-transformacion \
		--package-type Image \
		--code ImageUri=<reemplazar_con_AWS_account_id>.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest \
		--role arn:aws:iam::<reemplazar_con_AWS_account_id>:role/lambda-ex
	aws lambda invoke --function-name lambda-transformacion response.json
	