1. Test Django
```
	py manage.py test
```
2. Build container
```
	docker build -f Dockerfile \
		-t registry.digitalocean.com/cfe-k8s/scoutify:latest \
		-t registry.digitalocean.com/cfe-k8s/scoutify:v1 \
		.
```
3.  Push this container to the Digital Ocean Container Registry
```
	docker push registry.digitalocean.com/cfe-k8s/scoutify --all-tags
```

4. Update secrets
```
	kubetctl delete secret k8s-scoutify-prod-env
	kubetctl create secret generic k8s-scoutify-prod-env --from-env-file=scoutify/.env.prod
```

5. Update deployment
```
	kubectl apply -f k8s/apps/django-k8s-scoutify-yml
```

6. Wait for rollout to finish
```
	kubectl rollout status deployment/django-k8s-scoutify-deployment
```

7. Migrate database
```
	
```