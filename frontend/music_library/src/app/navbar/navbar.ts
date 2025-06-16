import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss'
})
export class NavbarComponent {

  isOpen = false; //determines whether the mobile navbar is toggled or not
  isDropdownOpen = false;

  /**
   * Handles user click on the navbar menu toggle on small screens
   */
  toggle() {
    this.isOpen = !this.isOpen;
  }

  /**
   * Closes the toggled navbar when a user clicks on a link
   */
  handleNavigationClick(){
    this.isOpen = false;
  }

  toggleDropdown(){
    this.isDropdownOpen = !this.isDropdownOpen;
  }
}
