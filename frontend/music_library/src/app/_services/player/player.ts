import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {
  private audio = new Audio();

  loadTrack(url: string) {
    this.audio.src = url;
    this.audio.load();
  }

  play() {
    this.audio.play();
  }

  pause() {
    this.audio.pause();
  }

  togglePlay() {
    this.audio.paused ? this.play() : this.pause();
  }

  isPaused(): boolean {
    return this.audio.paused;
  }

  getCurrentTime(): number {
    return this.audio.currentTime;
  }

  getDuration(): number {
    return this.audio.duration;
  }

  setCurrentTime(time: number) {
    this.audio.currentTime = time;
  }

  on(event: string, callback: (event: any) => void) {
    this.audio.addEventListener(event, callback);
  }

  setMetadata(title: string, artist: string, artworkUrl: string) {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title,
        artist,
        artwork: [
          { src: artworkUrl, sizes: '96x96', type: 'image/png' },
          { src: artworkUrl, sizes: '256x256', type: 'image/png' }
        ]
      });
    }
  }
}
