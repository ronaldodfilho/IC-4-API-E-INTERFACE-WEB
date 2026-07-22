<script setup>
import { computed, onMounted, ref } from "vue";
import { listarOperadoras } from "../services/api";

const operadoras = ref([]);

const carregando = ref(false)
const erro = ref('')
const pagina = ref(1);
const limite = ref(10);
const total = ref(0);
const busca = ref("");

async function carregarOperadoras() {
  carregando.value = true
  erro.value = ''

  try {
    const resposta = await listarOperadoras(
      pagina.value,
      limite.value,
      busca.value
    )

    operadoras.value = resposta.data
    total.value = resposta.total
  } catch (error) {
    console.error(error)
    erro.value = 'Não foi possível carregar as operadoras.'
    operadoras.value = []
  } finally {
    carregando.value = false
  }
}

function pesquisarOperadoras() {
  pagina.value = 1;
  carregarOperadoras();
}

function paginaAnterior() {
  if (pagina.value > 1) {
    pagina.value--;
    carregarOperadoras();
  }
}

function proximaPagina() {
  if (pagina.value * limite.value < total.value) {
    pagina.value++;
    carregarOperadoras();
  }
}

const totalPaginas = computed(() => {
  return Math.ceil(total.value / limite.value);
});

function formatarCnpj(cnpj) {
  const texto = cnpj.toString();

  return texto.replace(
    /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
    "$1.$2.$3/$4-$5",
  );
}

onMounted(async () => {
  carregarOperadoras();
});
</script>

<template>
  <main>
    <h1>Operadoras de saúde</h1>
    <p v-if="carregando">Carregando operadoras...</p>
    <p v-else-if="erro">{{ erro }}</p>
    <div class="pesquisa">
      <input v-model="busca" @input="pesquisarOperadoras" placeholder="Pesquisar por CNPJ ou Razão Social" />
      <button @click="pesquisarOperadoras">Pesquisar</button>
    </div>
    <table v-if="operadoras.length > 0">
      <thead>
        <tr>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>UF</th>
          <th>Modalidade</th>
          <th>Ações</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="operadora in operadoras" :key="operadora.cnpj">
          <td>{{ formatarCnpj(operadora.cnpj) }}</td>
          <td>{{ operadora.razao_social }}</td>
          <td>{{ operadora.uf }}</td>
          <td>{{ operadora.modalidade }}</td>
          <td>
            <RouterLink :to="{
              name: 'detalhes-operadora',
              params: { cnpj: operadora.cnpj },
            }">
              Ver detalhes
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Nenhuma operadora encontrada.</p>
    <p>página: {{ pagina }} de {{ totalPaginas }}</p>
    <div v-if="!carregando && !erro && operadoras.length > 0" class="paginacao">
      <button @click="paginaAnterior" :disabled="pagina === 1 || carregando">
        Anterior
      </button>

      <button @click="proximaPagina" :disabled="pagina * limite >= total || carregando">
        Próxima
      </button>
    </div>
  </main>
</template>
