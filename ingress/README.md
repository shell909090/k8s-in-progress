# ingress-nginx

```
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```

# traefik

```
helm upgrade --install traefik traefik/traefik -n traefik --create-namespace
```
