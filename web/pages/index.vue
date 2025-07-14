<template>
    <p>Redirecting...</p>
</template>
<script setup>

const router = useRouter()

onMounted(() => {
  router.push('/login') 
})

</script>