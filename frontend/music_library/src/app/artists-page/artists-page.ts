import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { Artist } from '../_services/rest-backend/artist.type'
import { RestBackendService } from '../_services/rest-backend/rest-backend';

@Component({
  selector: 'app-artists-page',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './artists-page.html',
  styleUrl: './artists-page.scss'
})
export class ArtistsPage {
  restService = inject(RestBackendService);
  router = inject(Router);
  artists: Artist[] = [];
  
  ngOnInit() {
    this.fetchArtists();  
  }
  
  fetchArtists(){
    this.restService.getArtists().subscribe({
      next: (data) => {
        console.log(data);
        this.artists = data;
      },
      error: (err) => {
        console.log(err);
        // if(err.status === 401){
        //   this.toastr.error("Your access token appears to be invalid. Login again", "Token expired");
        //   this.router.navigateByUrl("/login");
        // } else {
        //   this.toastr.error(err.message, err.statusText)
        // }
      }
    });
  }


}
