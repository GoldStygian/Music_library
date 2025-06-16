// player.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlayerService } from '../_services/player/player';

@Component({
  selector: 'app-player',
  standalone: true,
  templateUrl: './player.html',
  styleUrls: ['./player.scss'],
  imports: [CommonModule]
})
export class PlayerComponent implements OnInit {
  isPaused = true;
  currentTime = '00:00';
  progress = 0;
  trackTitle = 'Titolo della Canzone';
  trackArtist = '';
  trackCover = '';

  constructor(public player: PlayerService) {}

  ngOnInit(): void {
    this.player.on('timeupdate', () => {
      const current = this.player.getCurrentTime();
      const duration = this.player.getDuration() || 1;
      this.progress = (current / duration) * 100;
      this.currentTime = this.formatTime(current);
    });
  }

  togglePlayPause(): void {
    this.player.togglePlay();
    this.isPaused = this.player.isPaused();
  }

  onProgressChange(value: number): void {
    const duration = this.player.getDuration();
    this.player.setCurrentTime((value / 100) * duration);
  }

  changeTrack(url: string, title: string, artist: string, cover: string) {
    this.player.loadTrack(url);
    this.player.setMetadata(title, artist, cover);
    this.player.play();
    this.trackTitle = title;
    this.trackArtist = artist;
    this.trackCover = cover;
    this.isPaused = false;
  }

  formatTime(seconds: number): string {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
  }
}
