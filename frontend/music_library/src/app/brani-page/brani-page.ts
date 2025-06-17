import { Component, inject, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { Track } from '../_services/rest-backend/track.type'
import { RestBackendService } from '../_services/rest-backend/rest-backend';
import { PlayerComponent } from '../player/player';
import { PlayerService } from '../_services/player/player';


@Component({
  selector: 'app-brani-page',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './brani-page.html',
  styleUrl: './brani-page.scss'
})
export class BraniPage {
  restService = inject(RestBackendService);
  router = inject(Router);
  brani: Track[] = [];

  ngOnInit() {
    this.fetchBrani();  
  }

  onTrackClick(track: Track) {
    const url   = `${this.restService.media_url}/${track.file_name}`;
    const cover = `${this.restService.media_url}/Album/${track.album_id}.jpg`;

    // Emetti l'evento globale
    window.dispatchEvent(new CustomEvent('play-track', {
      detail: { url, title: track.title, artist: track.author, cover }
    }));
  }

  fetchBrani(){
    this.restService.getTracks().subscribe({
      next: (data) => {
        console.log(data);
        this.brani = data;
      },
      error: (err) => {
        console.log(err);
      }
    });
  }

  // playTrack(track: any) {
  //   console.log("Track changed\n");
  //   console.log(this.restService.media_url + '/' + track.author + '/' + track.title + '.mp3');
  //   this.player.changeTrack(
  //     this.restService.media_url + '/' + track.author + '/' + track.title + '.mp3',
  //     track.title,
  //     track.author,
  //     this.restService.media_url + '/' + track.author + '/cover.jpg'
  //   );
  // }

}
