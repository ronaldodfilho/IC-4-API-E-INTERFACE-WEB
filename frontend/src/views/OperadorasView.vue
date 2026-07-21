<script setup>
import { computed, onMounted, ref } from "vue";
import { listarOperadoras } from "../services/api";

const operadoras = ref([]);

const pagina = ref(1);
const limite = ref(10);
const total = ref(0);
const busca = ref("");

async function carregarOperadoras() {
  const resposta = await listarOperadoras(
    pagina.value,
    limite.value,
    busca.value,
  );
  operadoras.value = resposta.data;
  total.value = resposta.total;
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
    <div class="pesquisa">
      <input
        v-model="busca"
        @input="pesquisarOperadoras"
        placeholder="Pesquisar por CNPJ ou Razão Social"
      />
      <button @click="pesquisarOperadoras">Pesquisar</button>
    </div>
    <table>
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
            <RouterLink
              :to="{
                name: 'detalhes-operadora',
                params: { cnpj: operadora.cnpj },
              }"
            >
              Ver detalhes
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
    <p>página: {{ pagina }} de {{ totalPaginas }}</p>
    <div class="paginacao">
      <button @click="paginaAnterior" :disabled="pagina === 1">Anterior</button>
      <button @click="proximaPagina" :disabled="pagina * limite >= total">
        Próxima
      </button>
    </div>
  </main>
</template>
