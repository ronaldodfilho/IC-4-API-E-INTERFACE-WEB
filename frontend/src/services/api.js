const URL_BASE = "http://localhost:8000/api"

export async function listarOperadoras(page = 1, limit = 10, busca = "") {
  const parametros = new URLSearchParams({page,limit,busca});
  const resposta = await fetch(`${URL_BASE}/operadoras?${parametros}`);

  if (!resposta.ok) {
    throw new Error("Erro ao carregar operadoras");
  }

  return resposta.json();
}


export async function exibirDetalhesOperadora(cnpj) {
  const resposta = await fetch(`${URL_BASE}/operadoras/${cnpj}`);

  if (!resposta.ok) {
  throw new Error("Erro ao carregar detalhes da operadora");
  }

  return resposta.json();
}

export async function listarDespesas(cnpj) {
  const resposta = await fetch(`${URL_BASE}/operadoras/${cnpj}/despesas`);

  if (!resposta.ok) {
    throw new Error("Erro ao carregar despesas da operadora");
}
    return resposta.json();
}