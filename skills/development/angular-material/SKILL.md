---
name: angular-material
description: Use when working with Angular Material components, theming, or styling. Triggers on requests involving "material", "theme", "mat-", buttons, dialogs, forms, tables, or UI components.
---

# Angular Material Guide

Use Angular Material v3 components and theming following project patterns.

## Component Imports

Import Material components directly (standalone):

```typescript
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule } from '@angular/material/dialog';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatTabsModule } from '@angular/material/tabs';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

@Component({
  imports: [
    MatButtonModule,
    MatCardModule,
    // Only import what you need
  ],
})
```

## Common Component Patterns

### Buttons

```html
<!-- Basic buttons -->
<button mat-button>Basic</button>
<button mat-raised-button color="primary">Raised</button>
<button mat-flat-button color="accent">Flat</button>
<button mat-stroked-button>Stroked</button>
<button mat-icon-button aria-label="Settings">
  <mat-icon>settings</mat-icon>
</button>
<button mat-fab color="primary">
  <mat-icon>add</mat-icon>
</button>
<button mat-mini-fab color="warn">
  <mat-icon>delete</mat-icon>
</button>

<!-- Disabled state with signals -->
<button mat-raised-button [disabled]="loading()">Submit</button>
```

### Form Fields

```html
<mat-form-field appearance="outline">
  <mat-label>Email</mat-label>
  <input matInput type="email" [formControl]="emailControl" />
  <mat-icon matSuffix>email</mat-icon>
  <mat-hint>Enter your email address</mat-hint>
  @if (emailControl.hasError('email')) {
  <mat-error>Invalid email format</mat-error>
  }
</mat-form-field>

<!-- Select -->
<mat-form-field appearance="outline">
  <mat-label>Priority</mat-label>
  <mat-select [(value)]="selectedPriority">
    @for (option of priorities; track option.value) {
    <mat-option [value]="option.value">{{ option.label }}</mat-option>
    }
  </mat-select>
</mat-form-field>

<!-- Textarea -->
<mat-form-field appearance="outline">
  <mat-label>Description</mat-label>
  <textarea matInput rows="4" [formControl]="descriptionControl"></textarea>
  <mat-hint align="end">
    {{ descriptionControl.value?.length || 0 }}/500
  </mat-hint>
</mat-form-field>
```

### Cards

```html
<mat-card>
  <mat-card-header>
    <mat-card-title>{{ task().title }}</mat-card-title>
    <mat-card-subtitle>Due: {{ task().dueDate | date }}</mat-card-subtitle>
  </mat-card-header>
  <mat-card-content>
    <p>{{ task().description }}</p>
  </mat-card-content>
  <mat-card-actions align="end">
    <button mat-button (click)="onEdit()">Edit</button>
    <button mat-button color="warn" (click)="onDelete()">Delete</button>
  </mat-card-actions>
</mat-card>
```

### Dialog

```typescript
// dialog.ts
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';

export interface DialogData {
  title: string;
  message: string;
}

@Component({
  selector: 'app-confirm-dialog',
  imports: [MatDialogModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>{{ data.title }}</h2>
    <mat-dialog-content>
      <p>{{ data.message }}</p>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" [mat-dialog-close]="true">Confirm</button>
    </mat-dialog-actions>
  `,
})
export class ConfirmDialog {
  readonly data = inject<DialogData>(MAT_DIALOG_DATA);
}

// Usage in parent component
readonly dialog = inject(MatDialog);

openConfirmDialog(): void {
  const dialogRef = this.dialog.open(ConfirmDialogComponent, {
    width: '400px',
    data: { title: 'Confirm Delete', message: 'Are you sure?' },
  });

  dialogRef.afterClosed().subscribe(result => {
    if (result) {
      this.performDelete();
    }
  });
}
```

### Table with Pagination and Sorting

```typescript
import { MatTableDataSource } from "@angular/material/table";
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";

@Component({
  imports: [MatTableModule, MatPaginatorModule, MatSortModule],
  template: `
    <table mat-table [dataSource]="dataSource" matSort>
      <ng-container matColumnDef="name">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>Name</th>
        <td mat-cell *matCellDef="let row">{{ row.name }}</td>
      </ng-container>

      <ng-container matColumnDef="status">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>Status</th>
        <td mat-cell *matCellDef="let row">{{ row.status }}</td>
      </ng-container>

      <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
      <tr mat-row *matRowDef="let row; columns: displayedColumns"></tr>
    </table>

    <mat-paginator
      [pageSizeOptions]="[5, 10, 25]"
      showFirstLastButtons
    ></mat-paginator>
  `,
})
export class DataTable implements AfterViewInit {
  displayedColumns = ["name", "status"];
  dataSource = new MatTableDataSource<Item>();

  readonly paginator = viewChild(MatPaginator);
  readonly sort = viewChild(MatSort);

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator() ?? null;
    this.dataSource.sort = this.sort() ?? null;
  }
}
```

### Snackbar

```typescript
readonly snackBar = inject(MatSnackBar);

showSuccess(message: string): void {
  this.snackBar.open(message, 'Close', {
    duration: 3000,
    horizontalPosition: 'end',
    verticalPosition: 'top',
    panelClass: ['success-snackbar'],
  });
}

showError(message: string): void {
  this.snackBar.open(message, 'Dismiss', {
    duration: 5000,
    panelClass: ['error-snackbar'],
  });
}
```

## Theming

### Theme Configuration (styles.scss)

```scss
@use "@angular/material" as mat;

// Define palettes
$primary: mat.m2-define-palette(mat.$m2-indigo-palette);
$accent: mat.m2-define-palette(mat.$m2-pink-palette, A200, A100, A400);
$warn: mat.m2-define-palette(mat.$m2-red-palette);

// Create theme
$theme: mat.m2-define-light-theme(
  (
    color: (
      primary: $primary,
      accent: $accent,
      warn: $warn,
    ),
    typography: mat.m2-define-typography-config(),
    density: 0,
  )
);

// Apply theme
@include mat.all-component-themes($theme);

// Dark theme
$dark-theme: mat.m2-define-dark-theme(
  (
    color: (
      primary: $primary,
      accent: $accent,
      warn: $warn,
    ),
  )
);

.dark-theme {
  @include mat.all-component-colors($dark-theme);
}
```

### Component-Level Styling

```scss
// component.scss
@use "@angular/material" as mat;

:host {
  display: block;
}

.custom-card {
  @include mat.elevation(4);

  &:hover {
    @include mat.elevation(8);
  }
}
```

## CDK Utilities

```typescript
// Drag and Drop
import { CdkDragDrop, DragDropModule, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  imports: [DragDropModule],
  template: `
    <div cdkDropList (cdkDropListDropped)="drop($event)">
      @for (item of items(); track item.id) {
        <div cdkDrag>{{ item.name }}</div>
      }
    </div>
  `,
})
export class DragList {
  drop(event: CdkDragDrop<string[]>): void {
    moveItemInArray(this.items(), event.previousIndex, event.currentIndex);
  }
}

// Virtual Scrolling
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  imports: [ScrollingModule],
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      <div *cdkVirtualFor="let item of items()" class="item">
        {{ item.name }}
      </div>
    </cdk-virtual-scroll-viewport>
  `,
})
```

## Checklist

- [ ] Import only required Material modules
- [ ] Use `appearance="outline"` for form fields
- [ ] Provide proper `mat-label` for form fields
- [ ] Use `mat-error` for validation messages
- [ ] Include `aria-label` for icon buttons
- [ ] Use theme colors (`primary`, `accent`, `warn`)
- [ ] Apply proper elevation for cards and dialogs
