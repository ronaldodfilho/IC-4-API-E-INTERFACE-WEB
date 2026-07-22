<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { exibirDetalhesOperadora, listarDespesas } from "../services/api";

const route = useRoute();
const operadora = ref(null);
const despesas = ref([]);
const carregandoOperadora = ref(true)
const carregandoDespesas = ref(true)
const erroOperadora = ref('')
const erroDespesas = ref('')

async function carregarDetalhesOperadoras() {
  const cnpj = route.params.cnpj

  carregandoOperadora.value = true
  erroOperadora.value = ''

  try {
    const resposta = await exibirDetalhesOperadora(cnpj)
    operadora.value = resposta.data
  } catch (error) {
    console.error(error)
    erroOperadora.value = 'Não foi possível carregar os dados da operadora.'
  } finally {
    carregandoOperadora.value = false
  }
}

async function carregarDespesas() {
  const cnpj = route.params.cnpj

  carregandoDespesas.value = true
  erroDespesas.value = ''

  try {
    const resposta = await listarDespesas(cnpj)
    despesas.value = resposta.data
  } catch (error) {
    console.error(error)

    if (error.message.includes('404')) {
      despesas.value = []
    } else {
      erroDespesas.value = 'Não foi possível carregar as despesas.'
    }
  } finally {
    carregandoDespesas.value = false
  }
}

function formatarMoeda(valor) {
  return Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(valor);
}

function formatarCnpj(cnpj) {
  const texto = cnpj.toString();

  return texto.replace(
    /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
    "$1.$2.$3/$4-$5",
  );
}

onMounted(() => {
  carregarDetalhesOperadoras();
  carregarDespesas();
});
</script>

<template>
  <main>
    <RouterLink to="/operadoras"> ← Voltar para a lista </RouterLink>

    <p v-if="carregandoOperadora">
  Carregando dados da operadora...
</p>

<p v-else-if="erroOperadora">
  {{ erroOperadora }}
</p>

    <h1>Detalhes da Operadora</h1>

    <table v-if="operadora">
      <thead>
        <tr>
          <th>Registro ANS</th>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>Modalidade</th>
          <th>UF</th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td>{{ operadora.registro_ans }}</td>
          <td>{{ formatarCnpj(operadora.cnpj) }}</td>
          <td>{{ operadora.razao_social }}</td>
          <td>{{ operadora.modalidade }}</td>
          <td>{{ operadora.uf }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Despesas</h2>

    <p v-if="carregandoDespesas">Carregando despesas...</p>

    <table v-if="despesas.length > 0">
      <thead>
        <tr>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>Ano</th>
          <th>Trimestre</th>
          <th>Valor das Despesas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="despesa in despesas" :key="despesa.id">
          <td>{{ formatarCnpj(despesa.cnpj) }}</td>
          <td>{{ despesa.razao_social }}</td>
          <td>{{ despesa.ano }}</td>
          <td>{{ despesa.trimestre }}</td>
          <td>{{ formatarMoeda(despesa.valor_despesas) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Dados não encontrados.</p>
  </main>
</template>
