import { Routes } from '@angular/router';
import { ArtistsPage } from './artists-page/artists-page';
import { ArtistDetail } from './artist-detail/artist-detail';
import { SearchPage } from './search-page/search-page';
import { PlaylistPage } from './playlist-page/playlist-page';
import { BraniPage } from './brani-page/brani-page';
import { AlbumsPage } from './albums-page/albums-page';
import { UploadPage } from './upload-page/upload-page';

export const routes: Routes = [
    {
        path: '',
        redirectTo: "artisti",
        pathMatch: "full"
    },
    {
        path: 'artisti',
        component: ArtistsPage,
        title: 'Artisti'
    },
    {
        path: 'artisti/:id',
        component: ArtistDetail,
        title: 'Artista'
    },
    {
        path: 'ricerca',
        component: SearchPage,
        title: 'Ricerca'
    },
    {
        path: 'playlist',
        component: PlaylistPage,
        title: 'Playlist'
    },
    {
        path: 'brani',
        component: BraniPage,
        title: 'Brani'
    },
    {
        path: 'album',
        component: AlbumsPage,
        title: 'Album'
    },
        {
        path: 'upload',
        component: UploadPage,
        title: 'Upload'
    }
];
