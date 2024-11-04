<template>
    <div>
        <template v-if="loading">
            <v-progress-circular indeterminate></v-progress-circular>
        </template>
        <template v-else>
            <template v-if="lab.status !== 'Running'">
                <v-btn :icon="mdiPlay" variant="text" @click="upMachine" color="green"></v-btn>
            </template>
            <template v-else>
                <v-btn :icon="mdiRestart" variant="text" @click="restartMachine" color="yellow"></v-btn>
                <v-btn :icon="mdiStop" variant="text" @click="destroyMachine" color="red"></v-btn>
            </template>
        </template>
    </div>
</template>

<script>
import { mdiPlay, mdiRestart, mdiStop } from '@mdi/js'

export default {
    props: {
        lab: {
            id: Number(),
            status: String(),
        }
    },
    emits: ["update"],
    data() {
        return {
            running: false,
            loading: false,
        }
    },
    setup() {
        return {
            mdiPlay,
            mdiRestart,
            mdiStop,
        }
    },
    mounted() {
        if (this.lab.status == "Processing")
            this.loading = true
        else
            this.loading = false
    },
    methods: {
        upMachine() {
            this.loading = true
            this.$http.post('run', { "id": this.lab.id }).then(response => {
                if (response.data.status = "Running") {
                    this.$toast.success("Machine is UP")
                }
                else {
                    this.$toast.error("Machine is error deploying")
                }
                this.loading = false
                this.$emit('update')
            }).catch(e => {
                this.$toast.error(e.response.data.detail || "An error occurred")
                this.loading = false
                this.$emit('update')
            });
        },

        destroyMachine() {
            this.loading = true
            this.$http.post('destroy', { "id": this.lab.id }).then(response => {
                if (response.data.status == "Not created") {
                    this.$toast.success("Machine is destroyed")
                }
                else {
                    this.$toast.error("Machine is error destroying")
                }
                this.loading = false
                this.$emit('update')
            }).catch(e => {
                this.$toast.error(e.response.data.detail || "An error occurred")
                this.loading = false
                this.$emit('update')
            });
        },

        restartMachine() {
            this.loading = true
            this.$http.post('restart', { "id": this.lab.id }).then(response => {
                if (response.data.status == "Running") {
                    this.$toast.success("Machine is restarting")
                }
                else {
                    this.$toast.error("Machine is error restarting")
                }
                this.loading = false
                this.$emit('update')
            }).catch(e => {
                this.$toast.error(e.response.data.detail || "An error occurred")
                this.loading = false
                this.$emit('update')
            });
        }
    },
}
</script>

<style scoped></style>