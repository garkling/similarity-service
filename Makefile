help:
	@echo "Available commands:"
	@echo "make "
	@echo "     init-environment     - init virtual environment for local run"
	@echo "     create-cluster       - create Minikube cluster with default settings"
	@echo "     delete-cluster       - destroy Minikube cluster"
	@echo "     run-server-local     - run the web-server locally via Uvicorn (.env must be present)"
	@echo "     run-server-docker    - run the web-server via Docker (build + run) (.env must be present)"
	@echo "     run-server-cluster   - run the web-server via K8S cluster created earlier (.env must be present)"
	@echo "     run-cluster-proxy    - run a proxy to access the K8S service "
	@echo "     deployment-plan      - create & view the Terraform deployment plan"


init-environment:
	python3.12 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run-server-local:
	uvicorn src.main:app --reload --host localhost --port 8080

run-server-docker:
	docker build -t similarity-service-local -f Dockerfile .
	docker run --rm --name similarity-node -p "8080:8080" --env-file .env similarity-service-local

create-cluster:
	minikube start --cpus=2 --memory=2048 --driver=docker

delete-cluster:
	minikube delete

run-server-cluster:
	kubectl create secret generic web-envs \
  	--from-env-file=.env
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml

	kubectl get pods
	kubectl get services

run-cluster-proxy:
	minikube service similarity-service

deployment-plan:
	cd terraform && \
	terraform init && \
	terraform validate && \
	terraform plan
