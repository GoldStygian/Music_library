import { TestBed } from '@angular/core/testing';

import { RestBackendService } from './rest-backend';

describe('RestBackendService', () => {
  let service: RestBackendService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestBackendService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
