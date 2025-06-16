import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlbumsPage } from './albums-page';

describe('AlbumsPage', () => {
  let component: AlbumsPage;
  let fixture: ComponentFixture<AlbumsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlbumsPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlbumsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
