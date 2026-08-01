---
name: delontheme-integration
description: Implement ng-alain theming system with layout configuration, responsive
  design, menu management, and settings drawer for ng-lin project
---

---
name: @delon/theme Integration
description: Implement ng-alain theming system with layout configuration, responsive design, menu management, and settings drawer for ng-lin project
license: MIT
---

# @delon/theme Integration Skill

This skill guides the implementation of @delon/theme theming and layout system in the ng-lin construction site management system.

## When to Use This Skill

**Triggers**: "@delon/theme", "layout", "theme", "menu", "settings drawer", "responsive design", "alain layout"

Use this skill when:
- Configuring application layout and theming
- Managing navigation menus
- Implementing responsive layouts
- Adding settings drawer
- Customizing theme colors
- Working with layout components

## Core Theme Components

### 1. Layout Configuration

```typescript
import { Component } from '@angular/core';
import { LayoutDefaultComponent } from '@delon/theme/layout-default';
import { SettingDrawerComponent } from '@delon/theme/setting-drawer';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [LayoutDefaultComponent, SettingDrawerComponent],
  template: `
    <layout-default>
      <layout-default-header-item direction="left">
        <div class="logo">
          <img src="assets/logo.png" alt="GigHub" />
          <span>GigHub</span>
        </div>
      </layout-default-header-item>

      <layout-default-header-item direction="right">
        <app-user-menu />
      </layout-default-header-item>

      <router-outlet></router-outlet>
    </layout-default>

    <setting-drawer />
  `
})
export class LayoutComponent {}
```

### 2. Menu Configuration

```typescript
import { Component, inject, OnInit } from '@angular/core';
import { MenuService, Menu } from '@delon/theme';

@Component({
  selector: 'app-root',
  template: `<router-outlet />`
})
export class AppComponent implements OnInit {
  private menuService = inject(MenuService);

  ngOnInit(): void {
    this.menuService.add([
      {
        text: 'Dashboard',
        link: '/dashboard',
        icon: { type: 'icon', value: 'dashboard' }
      },
      {
        text: 'Blueprints',
        link: '/blueprints',
        icon: { type: 'icon', value: 'project' },
        children: [
          {
            text: 'All Blueprints',
            link: '/blueprints/list'
          },
          {
            text: 'Create Blueprint',
            link: '/blueprints/create'
          }
        ]
      },
      {
        text: 'Tasks',
        link: '/tasks',
        icon: { type: 'icon', value: 'check-square' },
        badge: 5,
        badgeStatus: 'processing'
      },
      {
        text: 'Reports',
        link: '/reports',
        icon: { type: 'icon', value: 'file-text' }
      }
    ]);
  }
}
```

### 3. Theme Settings

```typescript
import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { DelonConfig, AlainThemeModule } from '@delon/theme';

const delonConfig: DelonConfig = {
  theme: {
    layout: {
      alain: {
        // Layout mode: side | top
        mode: 'side',
        // Fixed header
        fixedHeader: true,
        // Fixed sidebar
        fixedSidebar: true,
        // Collapsed sidebar
        collapsed: false,
        // Display sidebar logo
        logo: true,
        // Sidebar width
        width: 200,
        // Collapsed sidebar width
        collapsedWidth: 64
      }
    },
    // Primary color
    primaryColor: '#1890ff',
    // Dark mode
    darkMode: false
  },
  // Page header configuration
  pageHeader: {
    home: '/',
    homeI18n: 'Home',
    recursiveBreadcrumb: true,
    autoBreadcrumb: true,
    autoTitle: true
  }
};

export const appConfig: ApplicationConfig = {
  providers: [
    importProvidersFrom(AlainThemeModule.forRoot(delonConfig))
  ]
};
```

### 4. Responsive Layout

```typescript
import { Component, inject } from '@angular/core';
import { LayoutDefaultOptions, ALAIN_LAYOUT_OPTIONS } from '@delon/theme/layout-default';
import { Platform } from '@angular/cdk/platform';

@Component({
  selector: 'app-responsive-layout',
  template: `
    <layout-default [options]="layoutOptions()">
      <router-outlet />
    </layout-default>
  `
})
export class ResponsiveLayoutComponent {
  private platform = inject(Platform);

  layoutOptions = computed(() => {
    const isMobile = this.platform.IOS || this.platform.ANDROID;

    return {
      logoExpanded: `assets/logo-full.png`,
      logoCollapsed: `assets/logo-icon.png`,
      hideAside: isMobile,
      displaySidebarCollapse: !isMobile,
      fixSiderbar: !isMobile,
      fixHeader: true
    } as LayoutDefaultOptions;
  });
}
```

### 5. Settings Drawer

```typescript
import { Component } from '@angular/core';
import { SettingDrawerComponent } from '@delon/theme/setting-drawer';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [SettingDrawerComponent],
  template: `
    <layout-default>
      <router-outlet />
    </layout-default>

    <!-- Settings drawer with theme customization -->
    <setting-drawer
      [data]="{
        layout: {
          fixed: true,
          collapsed: false,
          boxed: false,
          lang: null
        },
        theme: {
          color: '#1890ff',
          mode: 'light'
        }
      }"
      (dataChange)="onSettingsChange($event)" />
  `
})
export class AppComponent {
  onSettingsChange(settings: any): void {
    console.log('Settings changed:', settings);
    // Persist settings to localStorage or user preferences
  }
}
```

### 6. Dynamic Menu with Permissions

```typescript
import { Component, inject, OnInit, signal } from '@angular/core';
import { MenuService } from '@delon/theme';
import { PermissionService } from '@core/services/permission.service';

@Component({
  selector: 'app-menu-manager'
})
export class MenuManagerComponent implements OnInit {
  private menuService = inject(MenuService);
  private permissionService = inject(PermissionService);

  ngOnInit(): void {
    // Build menu based on user permissions
    const menu = this.buildMenu();
    this.menuService.add(menu);
  }

  private buildMenu(): Menu[] {
    const menu: Menu[] = [
      {
        text: 'Dashboard',
        link: '/dashboard',
        icon: { type: 'icon', value: 'dashboard' }
      }
    ];

    // Add Blueprint management if user has permission
    if (this.permissionService.canManageBlueprints()) {
      menu.push({
        text: 'Blueprints',
        link: '/blueprints',
        icon: { type: 'icon', value: 'project' },
        children: [
          {
            text: 'All Blueprints',
            link: '/blueprints/list'
          },
          {
            text: 'Create Blueprint',
            link: '/blueprints/create',
            acl: 'blueprint:create' // ACL permission check
          }
        ]
      });
    }

    // Add admin menu if user is admin
    if (this.permissionService.isAdmin()) {
      menu.push({
        text: 'Administration',
        icon: { type: 'icon', value: 'setting' },
        children: [
          {
            text: 'Users',
            link: '/admin/users'
          },
          {
            text: 'Organizations',
            link: '/admin/organizations'
          },
          {
            text: 'System Settings',
            link: '/admin/settings'
          }
        ]
      });
    }

    return menu;
  }
}
```

### 7. Custom Theme Colors

```less
// styles/theme.less
@import '~@delon/theme/index.less';

// Override primary color
@primary-color: #1890ff;

// Custom theme variables
@brand-primary: #1890ff;
@brand-success: #52c41a;
@brand-warning: #faad14;
@brand-error: #f5222d;

// Layout variables
@alain-default-aside-width: 200px;
@alain-default-aside-collapsed-width: 64px;
@alain-default-header-height: 64px;

// Custom component styles
.custom-layout {
  .alain-default__aside {
    background: linear-gradient(180deg, #001529 0%, #002140 100%);
  }

  .alain-default__header {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
}
```

## Integration Patterns

### Pattern 1: Layout with Blueprint Context

```typescript
import { Component, inject, signal, OnInit } from '@angular/core';
import { MenuService } from '@delon/theme';
import { BlueprintService } from '@core/services/blueprint.service';

@Component({
  selector: 'app-blueprint-layout',
  template: `
    <layout-default>
      <layout-default-header-item direction="left">
        <nz-select
          [(ngModel)]="selectedBlueprintId"
          (ngModelChange)="onBlueprintChange($event)"
          style="width: 200px">
          @for (bp of blueprints(); track bp.id) {
            <nz-option [nzValue]="bp.id" [nzLabel]="bp.name" />
          }
        </nz-select>
      </layout-default-header-item>

      <router-outlet />
    </layout-default>
  `
})
export class BlueprintLayoutComponent implements OnInit {
  private blueprintService = inject(BlueprintService);
  private menuService = inject(MenuService);

  blueprints = signal<Blueprint[]>([]);
  selectedBlueprintId = signal<string>('');

  ngOnInit(): void {
    this.loadBlueprints();
  }

  async loadBlueprints(): Promise<void> {
    const blueprints = await this.blueprintService.getUserBlueprints();
    this.blueprints.set(blueprints);

    if (blueprints.length > 0) {
      this.selectedBlueprintId.set(blueprints[0].id);
      this.updateMenuForBlueprint(blueprints[0].id);
    }
  }

  onBlueprintChange(blueprintId: string): void {
    this.updateMenuForBlueprint(blueprintId);
  }

  private updateMenuForBlueprint(blueprintId: string): void {
    this.menuService.add([
      {
        text: 'Dashboard',
        link: `/blueprints/${blueprintId}/dashboard`
      },
      {
        text: 'Tasks',
        link: `/blueprints/${blueprintId}/tasks`
      },
      {
        text: 'Reports',
        link: `/blueprints/${blueprintId}/reports`
      }
    ]);
  }
}
```

## Integration Checklist

When using @delon/theme:
- [ ] Configure layout options in app config
- [ ] Build menu structure with permissions
- [ ] Implement settings drawer for user customization
- [ ] Support responsive design (mobile/tablet/desktop)
- [ ] Customize theme colors in LESS/SCSS
- [ ] Integrate with ACL for menu visibility
- [ ] Handle Blueprint context in layout
- [ ] Persist user preferences (theme, layout, language)

## Best Practices

### DO ✅
- Use MenuService for dynamic menu management
- Implement responsive layout for mobile devices
- Integrate ACL permissions with menu items
- Persist theme settings to user preferences
- Use layout components from @delon/theme
- Customize theme colors via LESS variables

### DON'T ❌
- Hardcode menu structure in templates
- Ignore mobile/responsive requirements
- Skip ACL integration for menu items
- Use inline styles for theme customization
- Create custom layout components (use provided ones)

## References

- [ng-alain Layout Documentation](https://ng-alain.com/theme/layout/en)
- [Theme Configuration](https://ng-alain.com/theme/settings/en)
- [Menu Service](https://ng-alain.com/theme/menu/en)
- [Settings Drawer](https://ng-alain.com/components/setting-drawer/en)

---

**Version**: 1.0.0
**Compatible with**: @delon/theme 20.1.x, ng-alain 20.1.x
**Last Updated**: 2025-12-25
