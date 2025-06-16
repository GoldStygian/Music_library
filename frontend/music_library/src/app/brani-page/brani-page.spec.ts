import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BraniPage } from './brani-page';

describe('BraniPage', () => {
  let component: BraniPage;
  let fixture: ComponentFixture<BraniPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BraniPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BraniPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
