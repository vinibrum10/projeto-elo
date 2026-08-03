# Projeto Elo

Plataforma de dados que unifica fontes dispersas (planilhas e APIs)
em uma base única, servindo painéis que conectam dado à decisão.

## Problema

Dados operacionais espalhados em planilhas e sistemas distintos, sem
integração. Consolidação manual, recorrente e sujeita a erro.

## Arquitetura

Fontes → Extração (Python) → PostgreSQL (raw → staging → marts) → Metabase

## Status

Em desenvolvimento.