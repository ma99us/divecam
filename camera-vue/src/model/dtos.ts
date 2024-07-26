export class GpioPin {
  num?: number
  gpio?: number;
  wPi?: number;
  name?: string;
  mode?: number;
  v?: number;
}

export class PinAction {
  gpio?: number;
  wPi?: number;
  isHigh?: boolean;
  mode?: string;
  durationMs?: number;
  forward?: boolean;

  refresh: boolean = false;
}

export class TimeAction {
  hours?: number;
  minutes?: number;
  seconds?: number;
}

export class RebootAction {
  mode?: string
}

export class FindPicturesAction {
  offset?: number;
  limit?: number
}