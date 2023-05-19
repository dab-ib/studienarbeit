<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn v-bind="attrs" v-on="on" class="mx-2" fab dark color="orange">
        <v-icon dark>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Add Camera</span>
      </v-card-title>
      <v-card-text>
        <v-alert v-if="error" dense outlined type="error">
          {{ errorMessage }}
        </v-alert>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field label="name" required v-model="name"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="url"
                type="text"
                required
                v-model="url"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <template>
                <v-col cols="12">
                  <v-slider
                    v-model="minimum"
                    :max="3000"
                    :min="100"
                    label="Minimum object size"
                    class="align-center"
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="minimum"
                        class="mt-0 pt-0"
                        type="number"
                        style="width: 60px"
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
              </template>
            </v-col>
            <v-col cols="12">
              <template>
                <v-col cols="12">
                  <v-slider
                    v-model="maximum"
                    :max="3000"
                    :min="100"
                    label="Maximum object size"
                    class="align-center"
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="maximum"
                        class="mt-0 pt-0"
                        type="number"
                        style="width: 60px"
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
              </template>
            </v-col>
            <v-col cols="12">
              <template>
                <v-col cols="12">
                  <v-slider
                    v-model="threshold"
                    :max="3000"
                    :min="100"
                    label="Threshold"
                    class="align-center"
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="threshold"
                        class="mt-0 pt-0"
                        type="number"
                        style="width: 60px"
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
              </template>
            </v-col>
            <v-col cols="12">
              <template>
                <v-col cols="12">
                  <v-slider
                    v-model="sensitivity"
                    :max="3000"
                    :min="100"
                    label="Sensitivity settings"
                    class="align-center"
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="sensitivity"
                        class="mt-0 pt-0"
                        type="number"
                        style="width: 60px"
                      ></v-text-field>
                    </template>
</v-slider>
</v-col>
</template>
</v-col>
</v-row>
</v-container>
<small>*indicates required field</small>
</v-card-text>
<v-card-actions>
<v-spacer></v-spacer>
<v-btn color="blue darken-1" text @click="dialog = false">
Close
</v-btn>
<v-btn color="blue darken-1" text @click="addCamera()">
Save
</v-btn>
</v-card-actions>
</v-card>
</v-dialog>
</template>


<script>
  import CameraService from "../../services/CameraService";
  import { Camera } from "@/interfaces/CameraInterface";

  const cameraService = new CameraService();

  export default {
    name: "AddCameraDialog",
    data() {
      return {
        dialog: false,
        name: "",
        url: "",
        minimum: 0,
        maximum: 0,
        threshold: 0,
        sensitivity: 0,
        error: false,
        errorMessage: "",
      };
    },
    methods: {
      async addCamera() {
        try {
          const camera = new Camera(
            null,
            this.name,
            this.url,
            null,
            this.minimum,
            this.maximum,
            this.threshold,
            this.sensitivity
          );
          await cameraService.addCamera(camera);
          this.dialog = false;
        } catch (error) {
          this.error = true;
          this.errorMessage = "Error";
          //TODO: Fehlerbehandlung, wenn das Backend Fehlermeldungen zurückgibt
        }
      },
    },
  };
</script>


<style scoped>

</style>
