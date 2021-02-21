<template>
    <div>
        {{ q }}
    </div>
</template>

<script>
export default {
    data() {
        return {
            q: this.$route.query.p
        }
    },
}
</script>