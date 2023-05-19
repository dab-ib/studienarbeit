export interface CameraInterface {
    id: number | null;
    name: string;
    url: string;
    minimum: number;
    maximum: number;
    threshold: number;
    sensitivity: number
    last_motion: number | null;

}

export class Camera implements CameraInterface{
    id: number | null;
    name: string;
    url: string;
    minimum: number;
    maximum: number;
    threshold: number;
    sensitivity: number

    last_motion: number | null;

    public constructor(
        id: number | null,
         name: string, 
         url: string, 
         last_motion: number | null,
         minimum: number | 0,
         maximum: number | 500,
         threshold: number | 10,
         sensitivity: number | 500,
         ) {
        this.id = id
        this.name = name        
        this.url = url
        this.last_motion = last_motion
        this.minimum = minimum
        this.maximum = maximum
        this.threshold = threshold
        this.sensitivity = sensitivity
    }

    public getLastMotionAsDateString(): string {
            if (this.last_motion == null) {
                return "-"
            }
            return new Date(this.last_motion).toUTCString();
    }

}
