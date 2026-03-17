---
name: devexpress
description: |
  USE FOR: Building enterprise .NET applications using DevExpress UI components for Blazor, WinForms, WPF, or ASP.NET. Use when you need advanced data grids, reporting, scheduling, and rich editor components with commercial support.
  DO NOT USE FOR: Open-source-only projects (DevExpress requires a commercial license), lightweight prototypes where a full component suite is overkill, or game development.
license: MIT
metadata:
  displayName: DevExpress
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "DevExpress Documentation"
    url: "https://docs.devexpress.com/"
  - title: "DevExpress Official Site"
    url: "https://www.devexpress.com/"
---

# DevExpress

## Overview

DevExpress is a commercial UI component suite for .NET that provides hundreds of high-performance controls for Blazor, WPF, WinForms, and ASP.NET Core. The Blazor component library (DevExpress.Blazor) includes a Data Grid, Pivot Grid, Scheduler, Rich Text Editor, Charts, Reporting, and Layout components. DevExpress components are optimized for large datasets, enterprise workflows, and complex LOB (line-of-business) applications. They ship with built-in themes, localization, accessibility support, and extensive documentation.

## Blazor Data Grid Setup

Configure the DevExpress Blazor Data Grid with sorting, filtering, grouping, and editing.

```csharp
@page "/employees"
@using DevExpress.Blazor
@inject IEmployeeService EmployeeService

<DxGrid Data="_employees"
        KeyFieldName="Id"
        EditMode="GridEditMode.EditRow"
        EditModelSaving="OnEditModelSaving"
        PageSize="20"
        ShowFilterRow="true"
        ShowGroupPanel="true"
        ColumnResizeMode="GridColumnResizeMode.NextColumn">

    <Columns>
        <DxGridDataColumn FieldName="FirstName" Caption="First Name" Width="150px" />
        <DxGridDataColumn FieldName="LastName" Caption="Last Name" Width="150px" />
        <DxGridDataColumn FieldName="Department" Caption="Department" Width="200px">
            <FilterRowCellTemplate>
                <DxComboBox Data="_departments"
                            Value="(string)context.FilterRowValue"
                            ValueChanged="(string v) => context.FilterRowValue = v"
                            ClearButtonDisplayMode="DataEditorClearButtonDisplayMode.Auto" />
            </FilterRowCellTemplate>
        </DxGridDataColumn>
        <DxGridDataColumn FieldName="Salary" Caption="Salary" DisplayFormat="C0" Width="120px" />
        <DxGridDataColumn FieldName="HireDate" Caption="Hired" DisplayFormat="d" Width="120px" />
        <DxGridCommandColumn Width="160px">
            <CellDisplayTemplate>
                <DxButton Text="Edit" Click="() => context.Grid.StartEditRowAsync(context.VisibleIndex)"
                          RenderStyle="ButtonRenderStyle.Link" />
            </CellDisplayTemplate>
        </DxGridCommandColumn>
    </Columns>

    <TotalSummary>
        <DxGridSummaryItem SummaryType="GridSummaryItemType.Count" FieldName="Id" />
        <DxGridSummaryItem SummaryType="GridSummaryItemType.Avg" FieldName="Salary" DisplayFormat="Avg: {0:C0}" />
    </TotalSummary>
</DxGrid>

@code {
    private List<Employee> _employees = new();
    private List<string> _departments = new() { "Engineering", "Sales", "HR", "Finance" };

    protected override async Task OnInitializedAsync()
    {
        _employees = await EmployeeService.GetAllAsync();
    }

    private async Task OnEditModelSaving(GridEditModelSavingEventArgs e)
    {
        var editedEmployee = (Employee)e.EditModel;
        var dataItem = _employees.First(emp => emp.Id == editedEmployee.Id);

        dataItem.FirstName = editedEmployee.FirstName;
        dataItem.LastName = editedEmployee.LastName;
        dataItem.Department = editedEmployee.Department;
        dataItem.Salary = editedEmployee.Salary;

        await EmployeeService.UpdateAsync(dataItem);
    }
}
```

## Scheduler Component

The DxScheduler provides a full-featured calendar with appointments, resources, and recurrence rules.

```csharp
@page "/schedule"
@using DevExpress.Blazor

<DxScheduler StartDate="@DateTime.Today"
             DataStorage="_dataStorage"
             ActiveViewType="SchedulerViewType.WorkWeek"
             AppointmentInserted="OnAppointmentInserted"
             AppointmentUpdated="OnAppointmentUpdated"
             GroupType="SchedulerGroupType.Resource">

    <Views>
        <DxSchedulerDayView DayCount="1" ShowWorkTimeOnly="true"
                            WorkTime="new(TimeSpan.FromHours(8), TimeSpan.FromHours(18))" />
        <DxSchedulerWorkWeekView ShowWorkTimeOnly="true" />
        <DxSchedulerWeekView />
        <DxSchedulerMonthView />
    </Views>
</DxScheduler>

@code {
    private DxSchedulerDataStorage _dataStorage = new()
    {
        AppointmentsSource = new List<Appointment>(),
        AppointmentMappings = new DxSchedulerAppointmentMappings
        {
            Id = nameof(Appointment.Id),
            Start = nameof(Appointment.StartDate),
            End = nameof(Appointment.EndDate),
            Subject = nameof(Appointment.Subject),
            Description = nameof(Appointment.Description),
            LabelId = nameof(Appointment.LabelId),
            StatusId = nameof(Appointment.StatusId),
            ResourceId = nameof(Appointment.RoomId),
            RecurrenceInfo = nameof(Appointment.RecurrenceInfo)
        },
        ResourcesSource = new List<Room>
        {
            new() { Id = 1, Name = "Conference Room A", Color = System.Drawing.Color.Blue },
            new() { Id = 2, Name = "Conference Room B", Color = System.Drawing.Color.Green }
        },
        ResourceMappings = new DxSchedulerResourceMappings
        {
            Id = nameof(Room.Id),
            Caption = nameof(Room.Name),
            Color = nameof(Room.Color)
        }
    };

    private async Task OnAppointmentInserted(DxSchedulerAppointmentItem e)
    {
        var appointment = (Appointment)e.SourceObject;
        await AppointmentService.CreateAsync(appointment);
    }

    private async Task OnAppointmentUpdated(DxSchedulerAppointmentItem e)
    {
        var appointment = (Appointment)e.SourceObject;
        await AppointmentService.UpdateAsync(appointment);
    }
}
```

## Charts

DevExpress Blazor Charts support bar, line, area, pie, and financial chart types with interactive tooltips and zooming.

```csharp
@using DevExpress.Blazor

<DxChart Data="_salesData" Width="100%" Height="400px">
    <DxChartTitle Text="Quarterly Sales" />
    <DxChartBarSeries Name="Revenue"
                      ArgumentField="@((SalesRecord s) => s.Quarter)"
                      ValueField="@((SalesRecord s) => s.Revenue)"
                      Color="System.Drawing.Color.SteelBlue" />
    <DxChartLineSeries Name="Target"
                       ArgumentField="@((SalesRecord s) => s.Quarter)"
                       ValueField="@((SalesRecord s) => s.Target)"
                       Color="System.Drawing.Color.OrangeRed" />
    <DxChartLegend Position="RelativePosition.Outside"
                   HorizontalAlignment="HorizontalAlignment.Center"
                   VerticalAlignment="VerticalEdge.Bottom" />
    <DxChartTooltip Enabled="true">
        <ContentTemplate>
            <div>@($"{context.Point.Argument}: {context.Point.Value:C0}")</div>
        </ContentTemplate>
    </DxChartTooltip>
</DxChart>

@code {
    private readonly List<SalesRecord> _salesData = new()
    {
        new("Q1 2024", 120_000m, 100_000m),
        new("Q2 2024", 145_000m, 130_000m),
        new("Q3 2024", 138_000m, 140_000m),
        new("Q4 2024", 162_000m, 150_000m)
    };

    public record SalesRecord(string Quarter, decimal Revenue, decimal Target);
}
```

## DevExpress vs Other Blazor Component Libraries

| Feature | DevExpress | Telerik | Blazorise | MudBlazor |
|---|---|---|---|---|
| License | Commercial | Commercial | Open source + Pro | Open source |
| Grid performance (10K+ rows) | Virtual scrolling | Virtual scrolling | Server paging | Virtual scrolling |
| Built-in reporting | Yes (XtraReports) | Yes (Telerik Reporting) | No | No |
| Scheduler | Full-featured | Full-featured | Basic | No |
| Rich Text Editor | Yes | Yes | No | No |
| Pivot Grid | Yes | No | No | No |
| Blazor render modes | Server, WASM, SSR | Server, WASM, SSR | Server, WASM | Server, WASM |

## Best Practices

1. **Use `DxGrid` virtual scrolling mode (`VirtualScrollingEnabled="true"`) for datasets exceeding 500 rows** and bind to `IQueryable<T>` instead of `List<T>` so the grid translates sort/filter operations into LINQ expressions that execute server-side, avoiding loading the entire dataset into memory.

2. **Set `KeyFieldName` on every `DxGrid` instance to the primary key property** because DevExpress uses this field to track row identity during editing, selection, and focus operations; omitting it causes unpredictable behavior when rows are added or reordered.

3. **Configure `DxScheduler.DataStorage` field mappings using `nameof()` expressions** instead of hardcoded strings, so that property renames on the appointment or resource model produce compile-time errors rather than silent runtime failures.

4. **Create a shared DevExpress theme configuration in `App.razor` using `<DxResourceManager>` and set the global size mode** (`SizeMode.Small`, `Medium`, or `Large`) once, rather than setting `SizeMode` on individual components, which leads to inconsistent density across pages.

5. **Implement `GridEditModelSavingEventArgs` handlers that validate the `EditModel` and set `e.Cancel = true` on validation failure** with a user-visible notification, rather than silently ignoring invalid edits; the grid closes the edit row regardless unless `Cancel` is explicitly set.

6. **Use `DxGridDataColumn.DisplayFormat` with .NET format strings (e.g., `"C2"`, `"N0"`, `"d"`) on numeric and date columns** instead of formatting in `DisplayTemplate`, because `DisplayFormat` is used by the grid's built-in export, summary, and clipboard operations.

7. **Wrap chart data updates in `InvokeAsync(StateHasChanged)` when data arrives from background services or SignalR hubs** because `DxChart` relies on Blazor's render cycle to detect changes; mutating the data list without triggering a render produces stale visuals.

8. **Set explicit `Width` values on `DxGridDataColumn` for columns that display fixed-format data** (dates, currency, status badges) and leave only one text-heavy column without a width to absorb remaining space, preventing layout shifts during data loading.

9. **License the DevExpress NuGet feed using a `nuget.config` file with the DevExpress package source and credentials stored in CI environment variables**, not committed to source control; the DevExpress feed URL (`https://nuget.devexpress.com/api`) requires an active license key.

10. **Register DevExpress services before `builder.Build()` using `builder.Services.AddDevExpressBlazor()`** and add the `<DxResourceManager>` component in the `<head>` section of `App.razor` to ensure CSS and JavaScript resources are loaded before any DevExpress component renders.
