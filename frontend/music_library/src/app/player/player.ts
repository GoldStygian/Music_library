// player.component.ts
import { Component, OnInit, OnChanges, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlayerService } from '../_services/player/player';
// import { Track } from '../_services/rest-backend/track.type';

@Component({
  selector: 'app-player',
  standalone: true,
  templateUrl: './player.html',
  styleUrls: ['./player.scss'],
  imports: [CommonModule]
})
export class PlayerComponent implements OnInit, AfterViewInit, OnChanges {
  @ViewChild('titleRef', { static: false }) titleElement!: ElementRef;

  shouldScroll = false;

  isPaused = true;
  currentTime = '00:00';
  progress = 0;
  trackTitle = 'Titolo della Canzone';
  trackArtist = '';
  trackCover = '';

  // private queue: Track[];
  private queue: { url: string; title: string; artist: string; cover: string }[] = [];
  private index = -1;


  constructor(public player: PlayerService) {}

  ngOnInit(): void {
    this.player.on('timeupdate', () => {
      const current = this.player.getCurrentTime();
      const duration = this.player.getDuration() || 1;
      this.progress = (current / duration) * 100;
      this.currentTime = this.formatTime(current);
    });

    // Ascolta l'evento globale "play-track"
    window.addEventListener('play-track', (e: any) => {
      const { url, title, artist, cover } = e.detail;
      this.changeTrack(url, title, artist, cover);
    });
  }

  togglePlayPause(): void {
    this.player.togglePlay();
    this.isPaused = this.player.isPaused();
  }

  onProgressChange(value: number): void {
    console.log("[progress bar] " + value);
    const duration = this.player.getDuration();
    this.player.setCurrentTime((value / 100) * duration);
  }

  changeTrack(url: string, title: string, artist: string, cover: string) {

    this.trackTitle = title;

    console.log('[player] changeTrack chiamato con:');
    console.log('[player] URL:', url);
    console.log('[player] Title:', title);
    console.log('[player] Artist:', artist);
    console.log('[player] Cover:', cover);

    this.index = this.queue.findIndex(t => t.url === url);
    if (this.index < 0) {
      this.queue.push({ url, title, artist, cover });
      this.index = this.queue.length - 1;
    }
    
    setTimeout(() => this.checkIfTitleOverflows(), 0); // Controlla dopo il render

    this.player.loadTrack(url);
    this.player.setMetadata(title, artist, cover);
    this.player.play();
    this.trackTitle = title;
    this.trackArtist = artist;
    this.trackCover = cover;
    this.isPaused = false;
  }

  prevTrack() {
    if (this.index > 0) {
      const t = this.queue[--this.index];
      this.changeTrack(t.url, t.title, t.artist, t.cover);
    }
  }

  nextTrack() {
    if (this.index < this.queue.length - 1) {
      const t = this.queue[++this.index];
      this.changeTrack(t.url, t.title, t.artist, t.cover);
    }
  }

  ngAfterViewInit() {
    this.checkIfTitleOverflows();
  }

  ngOnChanges() {
    this.checkIfTitleOverflows();
  }

  checkIfTitleOverflows() {
    setTimeout(() => {
      const el = this.titleElement.nativeElement;
      this.shouldScroll = el.scrollWidth > el.clientWidth;
    });
  }

  formatTime(seconds: number): string {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
  }
}
