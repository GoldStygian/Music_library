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
  imports: [CommonModule, RouterModule, PlayerComponent],
  templateUrl: './brani-page.html',
  styleUrl: './brani-page.scss'
})
export class BraniPage {
  @ViewChild(PlayerComponent) player!: PlayerComponent;
  restService = inject(RestBackendService);
  router = inject(Router);
  brani: Track[] = [];

  ngOnInit() {
    this.fetchBrani();  
    this.player.changeTrack(
      this.restService.media_url + '/' + 'Lady Gaga' + '/' + 'Lady Gaga - Just Dance.mp3',
      'Lady Gaga',
      'Lady Gaga',
      this.restService.media_url + '/' + 'Lady Gaga' + '/cover.jpg'
    );
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

  playTrack(track: any) {
    console.log("Track changed\n");
    console.log(this.restService.media_url + '/' + track.author + '/' + track.title + '.mp3');
    this.player.changeTrack(
      this.restService.media_url + '/' + track.author + '/' + track.title + '.mp3',
      track.title,
      track.author,
      this.restService.media_url + '/' + track.author + '/cover.jpg'
    );
  }

}
