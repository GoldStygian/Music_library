import { Component, inject } from '@angular/core';
import { RestBackendService } from '../_services/rest-backend/rest-backend';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { HttpEvent, HttpEventType } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-upload-page',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './upload-page.html',
  styleUrl: './upload-page.scss'
})
export class UploadPage {
  restService = inject(RestBackendService);
  router = inject(Router);

  selectedFiles: File[] = [];
  variant: boolean = false;
  messages: string[] = [];

  onFilesSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files) return;
    this.selectedFiles = Array.from(input.files);
  }

  onSubmit(event: Event): void {
    event.preventDefault();
    if (this.selectedFiles.length === 0) {
      this.messages.push('Seleziona almeno un file.');
      return;
    }
    this.restService.uploadTracks(this.selectedFiles, this.variant).subscribe((event: HttpEvent<any>) => {
        if (event.type === HttpEventType.Response) {
          // Il server risponde con un array di { file, message }
          for (const res of event.body) {
            this.messages.push(res.message);
          }
        }
      }, err => {
        this.messages.push('Errore di rete o del server.');
      });
  }

}
