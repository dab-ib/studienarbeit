<template>
  <div class="overview">
    <v-container>
      <div>
        <v-row>
          <div class="camera" v-for="cam in cameraArray" :key="cam.id">
            <v-card class="mx-auto mr-5 mt-5" max-width="400">
              <div class="camera-image-wrapper">
                <img :src="getStreamPath(cam.id)" :id="'stream.' + cam.id" width="100%" />
                <canvas :id="'overlay.' + cam.id" class="camera-overlay"></canvas>
              </div>
              <v-card-subtitle class="pb-0">
                {{ cam.name }}
              </v-card-subtitle>
              <v-card-text class="text--primary">
                {{ cam.url }}
              </v-card-text>
              <v-card-text class="text--primary">
                Last Motion: {{ getLastMotionAsString(cam) }}
              </v-card-text>
              <v-card-actions class="justify-center">
                <v-btn color="orange" :to="getStreamUrl(cam.id)" text>
                  Open
                </v-btn>
                <v-btn color="orange" text>
                  <EditCameraDialog :cam="cam" />
                </v-btn>
                <DeleteCameraDialog :cam="cam" />
              </v-card-actions>
            </v-card>
          </div>

          <div class="camera__add">
            <v-card class="mx-auto mr-5 mt-5" width="320" height="240">
              <v-card-actions class="addBtn__wrapper justify-center align-center">
                <AddCameraDialog />
              </v-card-actions>
            </v-card>
          </div>
        </v-row>
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import WsStreams from '@/components/WsStreams.vue';
  import AddCameraDialog from '@/components/Camera/AddCameraDialog.vue';
  import DeleteCameraDialog from '@/components/Camera/DeleteCameraDialog.vue';
  import { cameraStoreMutations, cameraStoreState } from '@/store/CameraStore';
  import EditCameraDialog from '@/components/Camera/EditCameraDialog.vue';
  import { Camera } from "@/interfaces/CameraInterface";


  @Component({
    components: {
      EditCameraDialog,
      WsStreams,
      AddCameraDialog,
      DeleteCameraDialog,
    },
  })
  export default class Overview extends Vue {
    streamPath: string = process.env.VUE_APP_BACKEND_URL + '/streams/';

    get cameraArray(): Array<Camera> {
      return cameraStoreState.camerasArray;
    }

    async created() {
      await cameraStoreMutations.getList();


      // WS-Socket for Motion
      const connection = new WebSocket(process.env.VUE_APP_BACKEND_WS_URL);
      connection.onmessage = (e: MessageEvent) => {
        const event = JSON.parse(e.data);
        if (event.event === 'MotionResult' && event.data.motion) {
          const camera = cameraStoreMutations.get(event.data.camera.id);
          if (camera) {
            camera.last_motion = Date.now();
            const image = document.getElementById('stream.' + event.data.camera.id) as HTMLImageElement;
            if (image) {
              const scale = image.width / image.naturalWidth;
              const canvas = document.getElementById('overlay.' + event.data.camera.id) as HTMLCanvasElement;
              if (canvas) {
                const ctx = canvas.getContext('2d');
                if (ctx) {
                  ctx.clearRect(0, 0, canvas.width, canvas.height);
                  ctx.fillStyle = 'blue';
                  event.data.boxes.forEach((box: number[]) => {
                    box = box.map((x) => x * scale);
                    ctx.lineWidth = 5;
                    ctx.strokeStyle = 'green';
                    ctx.strokeRect(box[0], box[1], box[2], -box[3]);
                  });
                }
              }
            }
          }
        }
      };
    }

getStreamPath(cameraId: number): string {
  return this.streamPath + cameraId;
}

getLastMotionAsString(camera: Camera): string {
  if (camera.last_motion) {
    const lastMotionDate = new Date(camera.last_motion);
    return lastMotionDate.toLocaleString();
  }
  return 'N/A';
}

getStreamUrl(cameraId: number): string {
  return '/stream/' + cameraId;
}

  }
</script>

<style>
  .addBtn__wrapper {
    height: 100%;
  }

  .addBtn__wrapper .addBtn {
    width: 50px;
  }

  .motion {
    border: 2px solid red;
  }
</style>
