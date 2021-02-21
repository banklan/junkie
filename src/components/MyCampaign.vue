<template>
    <div>
        <h1>{{ slug }}</h1>
    </div>
</template>


<script>
export default {
    data() {
        return {
            id: this.$route.params.id,
            slug: this.$route.params.slug,
        }
    },
}
</script>