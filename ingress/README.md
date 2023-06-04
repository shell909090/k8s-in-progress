# ingress-nginx

```
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```

# traefik

```
helm upgrade traefik -n traefik -f traefik-values.yaml .
```
