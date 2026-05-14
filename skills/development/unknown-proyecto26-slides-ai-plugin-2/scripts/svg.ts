function toDataUri(svg: string): string {
  return 'data:image/svg+xml;base64,' + Buffer.from(svg).toString('base64');
}

export function sanitizeSvg(svg: string): string {
  let inner = svg;
  const a = inner.indexOf('<svg');
  const b = inner.indexOf('</svg>');
  if (a !== -1 && b !== -1) inner = inner.slice(a, b + 6);
  inner = inner.replace(/<\?xml[^>]*>/g, '');
  if (!/xmlns="http:\/\/www\.w3\.org\/2000\/svg"/.test(inner)) {
    inner = inner.replace(/<svg /, '<svg xmlns="http://www.w3.org/2000/svg" ');
  }
  inner = inner.replace(/(width|height)="([0-9.]+)(ex|em)"/g, (_m: string, attr: string, num: string) => {
    const px = Math.round(parseFloat(num) * 8.5);
    return `${attr}="${px}px"`;
  });
  inner = inner.replace(/currentColor/g, '#000000');
  return inner;
}

export function svgToDataUri(svg: string): string {
  return toDataUri(sanitizeSvg(svg));
}
