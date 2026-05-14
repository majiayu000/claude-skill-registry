// Type definitions for pptxgenjs-helpers
// All interfaces used across the helper modules

/** Color string in hex format (e.g., "FFFFFF" or "000000") */
export type ColorHex = string;

/** Dimension in inches */
export type InchesUnit = number;

/** Font size in points */
export type PointsUnit = number;

/** Shadow configuration for shapes and text */
export interface ShadowConfig {
  type: 'outer' | 'inner';
  color: ColorHex;
  opacity: number;
  angle?: number;
  blur?: number;
  offset?: number;
}

/** Font configuration including family names for different roles */
export interface FontConfig {
  heading: string;
  body: string;
  mono: string;
}

/** Font size ranges for different text roles */
export interface SizeConfig {
  title: { min: number; max: number };
  heading: { min: number; max: number };
  body: { min: number; max: number };
  caption: { min: number; max: number };
}

/** Spacing configuration in inches */
export interface SpacingConfig {
  margin: number;
  gutter: number;
  cardPad: number;
}

/** Border radius configuration in inches */
export interface RadiusConfig {
  card: number;
  badge: number;
}

/** Theme configuration that can be overridden */
export interface ThemeConfig {
  bg: { primary: ColorHex; secondary: ColorHex };
  text: { primary: ColorHex; secondary: ColorHex };
  accent: ColorHex;
  accentSecondary: ColorHex;
  font?: Partial<FontConfig>;
  size?: Partial<SizeConfig>;
  spacing?: Partial<SpacingConfig>;
  radius?: Partial<RadiusConfig>;
  shadow?: Partial<Record<string, ShadowConfig>>;
}

/** Fully resolved theme with all required properties */
export interface SlideTheme {
  bg: { primary: ColorHex; secondary: ColorHex };
  text: { primary: ColorHex; secondary: ColorHex };
  accent: ColorHex;
  accentSecondary: ColorHex;
  font: FontConfig;
  size: SizeConfig;
  spacing: SpacingConfig;
  radius: RadiusConfig;
  shadow: Record<string, ShadowConfig>;
}

/** A single validation issue found in a presentation */
export interface ValidationIssue {
  slide: number;
  type: string;
  message: string;
  severity: 'low' | 'medium' | 'high';
}

/** Result of validating a presentation deck */
export interface ValidationReport {
  passed: boolean;
  issues: ValidationIssue[];
  warnings: ValidationIssue[];
  stats: {
    slideCount: number;
    avgFontSize: number;
    minFontSize: number;
    hasNotes: boolean;
  };
}

/** Code token with styling information */
export interface CodeRun {
  text: string;
  options: {
    fontFace: string;
    color: ColorHex;
    fontSize: number;
  };
}

/** Image dimensions and aspect ratio */
export interface ImageDimensions {
  width: number;
  height: number;
  aspectRatio: number;
  type: 'png' | 'jpeg' | 'gif' | 'webp' | 'svg';
}

/** Image sizing result using crop */
export interface ImageSizingCropResult {
  x: InchesUnit;
  y: InchesUnit;
  w: InchesUnit;
  h: InchesUnit;
  sizing: {
    type: 'crop';
    x: InchesUnit;
    y: InchesUnit;
    w: InchesUnit;
    h: InchesUnit;
  };
}

/** Image sizing result using contain */
export interface ImageSizingContainResult {
  x: InchesUnit;
  y: InchesUnit;
  w: InchesUnit;
  h: InchesUnit;
}

/** Options for automatic font sizing */
export interface AutoFontSizeOpts {
  x?: number;
  y?: number;
  w: number;
  h: number;
  fontSize?: number;
  minFontSize?: number;
  maxFontSize?: number;
  mode?: 'auto' | 'shrink' | 'enlarge';
  italic?: boolean;
  bold?: boolean;
  fontStyle?: 'normal' | 'italic';
  fontWeight?: 'normal' | 'bold';
  leading?: number;
  margin?: number | { left?: number; top?: number; right?: number; bottom?: number };
  padding?: number;
  paraSpaceAfter?: number;
  fit?: 'shrink';
}

/** Options for calculating text box dimensions */
export interface TextBoxOpts extends AutoFontSizeOpts {
  text?: string | TextRun[];
  fontFace?: string;
  lines?: number;
}

/** A run of styled text */
export interface TextRun {
  text: string;
  options?: Partial<AutoFontSizeOpts>;
}

/** Calculated text box layout */
export interface TextBoxLayout {
  w: number | null;
  h: number;
  lines: number;
  contentH: number;
  margins: {
    left: number;
    right: number;
    top: number;
    bottom: number;
  };
  topInset: number;
}

/** Options for addStaircase decoration */
export interface StaircaseOpts {
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  color?: ColorHex;
  steps?: number;
  stepWidth?: number;
  stepHeight?: number;
  opacity?: number;
}

/** Options for addSectionBadge decoration */
export interface BadgeOpts {
  x?: number;
  y?: number;
}

/** Options for addProgressBar decoration */
export interface ProgressBarOpts {
  position?: 'top' | 'bottom';
  height?: number;
}

/** Options for addFeatureGrid layout builder */
export interface FeatureGridOpts {
  region: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
  features: Array<{
    title: string;
    desc?: string;
  }>;
}

/** Options for addCardRow layout builder */
export interface CardRowOpts {
  x?: number;
  y?: number;
  width?: number;
  gap?: number;
  image?: {
    path?: string;
    data?: string | Buffer;
    sizing?: 'crop' | 'contain';
    boxHeight?: number;
    crop?: {
      cx?: number;
      cy?: number;
      cw?: number;
      ch?: number;
    };
  };
  text?: string;
  textBox?: {
    fontSize?: number;
    fontFace?: string;
    h?: number;
    mode?: 'auto' | 'shrink' | 'enlarge';
    minFontSize?: number;
    maxFontSize?: number;
    margin?: number | Record<string, number>;
    paraSpaceAfter?: number;
    color?: ColorHex;
    align?: string;
    valign?: string;
  };
  background?: Record<string, any>;
}

/** Options for addTimeline layout builder */
export interface TimelineOpts {
  region: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
  milestones: Array<{
    date?: string;
    title?: string;
  }>;
}

/** Options for addMetricsRow layout builder */
export interface MetricsRowOpts {
  region: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
  metrics: Array<{
    value: string | number;
    label?: string;
  }>;
}

/** Options for addComparisonTable layout builder */
export interface ComparisonTableOpts {
  region: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
  data: {
    leftHeader?: string;
    rightHeader?: string;
    items: Array<{
      left?: string;
      right?: string;
    }>;
  };
}

/** Element position comparison result */
export interface ElementComparisonResult {
  relation: 'disjoint' | 'overlapping' | 'contained' | 'touching';
  containerIndex: number | null;
  containedIndex: number | null;
  aBounds: Record<string, number>;
  bBounds: Record<string, number>;
  intersection: { x: number; y: number; w: number; h: number } | null;
}

/** Slide dimensions in inches */
export interface SlideDimensions {
  width: number;
  height: number;
  source: 'detected' | 'emu_converted' | 'default';
}

/** Overlap warning options */
export interface OverlapWarningOpts {
  muteContainment?: boolean;
  ignoreLines?: boolean;
  ignoreDecorativeShapes?: boolean;
}

/** Image sizing options */
export interface ImageSizingOpts {
  cx?: number;
  cy?: number;
  cw?: number;
  ch?: number;
}

/** Code rendering options */
export interface CodeRunOpts {
  lang?: string;
}
