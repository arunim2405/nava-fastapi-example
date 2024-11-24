run-build:
	docker build -t org-management .

run-server:
	docker run -p 8000:8000 org-management

run: run-build run-server