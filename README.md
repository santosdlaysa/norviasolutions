# Norvia Solutions

Site institucional da Norvia Solutions — estúdio de software com aplicativos mobile (Doce Preço, Orgenyx, Organiza Ela) e sistemas web (AgroNet, Chef Flow, AgendaMais, Lumera Fest, Daex).

## Stack

- React 18 + TypeScript
- Vite
- React Router (landing page + página de detalhe por produto)
- CSS puro com design tokens (sem framework de CSS)

## Rodando localmente

```bash
npm install
npm run dev
```

## Build de produção

```bash
npm run build
```

O resultado fica em `dist/`. O `vercel.json` já contém o rewrite de SPA para as rotas `/produtos/:slug` funcionarem na Vercel.

## Onde editar

- **Produtos, links e textos**: `src/data/products.ts` (tudo é data-driven — adicionar um produto novo é adicionar um objeto no array)
- **Cores e tipografia**: tokens em `src/styles/globals.css` (`:root`)
- **E-mail de contato e redes sociais**: também em `src/data/products.ts`
