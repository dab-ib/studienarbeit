<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <!-- ... der restliche Code bleibt unverändert ... -->
    <v-card-text>
      <!-- ... der restliche Code bleibt unverändert ... -->
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-text-field
              label="name"
              required
              v-model="editedCam.name"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <template>
              <v-col cols="12">
                <v-slider
                  v-model="editedCam.minimum"
                  :max="3000"
                  :min="100"
                  type="number"
                  label="Minimum object size"
                  class="align-center"
                >
                  <!-- ... der restliche Code bleibt unverändert ... -->
                </v-slider>
              </v-col>
            </template>
          </v-col>
          <v-col cols="12">
            <template>
              <v-col cols="12">
                <v-slider
                  v-model="editedCam.maximum"
                  :max="3000"
                  :min="100"
                  type="number"
                  label="Maximum object size"
                  class="align-center"
                >
                  <!-- ... der restliche Code bleibt unverändert ... -->
                </v-slider>
              </v-col>
            </template>
          </v-col>
          <v-col cols="12">
            <template>
              <v-col cols="12">
                <v-slider
                  v-model="editedCam.threshold"
                  :max="3000"
                  :min="100"
                  type="number"
                  label="Threshold"
                  class="align-center"
                >
                  <!-- ... der restliche Code bleibt unverändert ... -->
                </v-slider>
              </v-col>
            </template>
          </v-col>
          <v-col cols="12">
            <template>
              <v-col cols="12">
                <v-slider
                  v-model="editedCam.sensitivity"
                  :max="3000"
                  :min="100"
                  type="number"
                  label="Sensitivity settings"
                  class="align-center"
                >
                  <!-- ... der restliche Code bleibt unverändert ... -->
                </v-slider>
              </v-col>
            </template>
          </v-col>
        </v-row>
      </v-container>
      <small>*indicates required field</small>
    </v-card-text>
    <!-- ... der restliche Code bleibt unverändert ... -->
  </v-dialog>
</template>

<script>
import CameraService from "../../services/CameraService";
import { Camera } from "@/interfaces/CameraInterface";

const cameraService = new CameraService();
export default {
  name: "EditCameraDialog",
  data() {
    return {
      dialog: false,
      error: false,
      errorMessage: "",
      editedCam: null, // Eine neue Datenvariable für die Änderungen
    };
  },
  props: {
    cam: Object,
  },
  watch: {
    cam:
{
immediate: true,
handler(newValue) {
// Beim Empfangen einer neuen Prop cam den Wert in editedCam kopieren
this.editedCam = { ...newValue };
},
},
},
methods: {
async updateCamera() {
await cameraService
.updateCamera(
new Camera(
this.editedCam.id,
this.editedCam.name,
this.editedCam.url,
this.editedCam.last_motion,
this.editedCam.minimum,
this.editedCam.maximum,
this.editedCam.threshold,
this.editedCam.sensitivity
)
)
.then((res) => {
if (res.status === 201) {
this.dialog = false;
} else {
this.error = true;
this.errorMessage = "Error";
// TODO: Fehlerbehandlung, falls der Backend-Fehlermeldungen zurückgibt
}
});
},
},
};
</script>

<style scoped>
/* ... der restliche Code bleibt unverändert ... */
</style>