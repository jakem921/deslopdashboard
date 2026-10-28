// measure: a small, exact image-measurement tool for design teardown.
//   measure <img> color x y                       -> hex at (x,y) (3x3 median)
//   measure <img> scan h|v <at> <from> <to> [thr] -> positions where luminance jumps by > thr (default 12): edges along a line
//   measure <img> ink  x0 y0 x1 y1 [thr]          -> background = mode colour of region; bbox of pixels differing > thr,
//                                                    plus ink rows (y-runs) and ink columns (x-runs) inside the region
//   measure <img> mode x0 y0 x1 y1                -> the most common colour in a region (a surface's fill)
//   measure <img> peak x0 y0 x1 y1                -> text colour of a region: the pixel furthest from its background
// Coordinates are image pixels, origin top-left.
import AppKit

let a = CommandLine.arguments
guard a.count >= 3, let img = NSImage(contentsOfFile: a[1]),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("bad args/image"); exit(1) }
let W = cg.width, H = cg.height
var buf = [UInt8](repeating: 0, count: W * H * 4)
let ctx = CGContext(data: &buf, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(cg, in: CGRect(x: 0, y: 0, width: W, height: H))
func px(_ x: Int, _ y: Int) -> (Int, Int, Int) {
    let i = (min(max(y, 0), H - 1) * W + min(max(x, 0), W - 1)) * 4
    return (Int(buf[i]), Int(buf[i + 1]), Int(buf[i + 2]))
}
func lum(_ c: (Int, Int, Int)) -> Double { 0.2126 * Double(c.0) + 0.7152 * Double(c.1) + 0.0722 * Double(c.2) }
func hex(_ c: (Int, Int, Int)) -> String { String(format: "#%02X%02X%02X", c.0, c.1, c.2) }
func dist(_ p: (Int, Int, Int), _ q: (Int, Int, Int)) -> Int { max(abs(p.0 - q.0), abs(p.1 - q.1), abs(p.2 - q.2)) }
func runs(_ flags: [Bool], offset: Int, minGap: Int = 2) -> [(Int, Int)] {
    var out: [(Int, Int)] = []; var start: Int? = nil; var gap = 0
    for (i, f) in flags.enumerated() {
        if f { if start == nil { start = i }; gap = 0 }
        else if let s = start { gap += 1; if gap > minGap { out.append((s + offset, i - gap + offset)); start = nil; gap = 0 } }
    }
    if let s = start { out.append((s + offset, flags.count - 1 - gap + offset)) }
    return out
}
func modeColor(_ x0: Int, _ y0: Int, _ x1: Int, _ y1: Int) -> (Int, Int, Int) {
    var counts: [Int: Int] = [:]
    for y in stride(from: y0, through: y1, by: 1) { for x in stride(from: x0, through: x1, by: 1) {
        let c = px(x, y); let k = (c.0 >> 2) << 16 | (c.1 >> 2) << 8 | (c.2 >> 2); counts[k, default: 0] += 1 } }
    let k = counts.max { $0.value < $1.value }!.key
    return ((k >> 16 & 0xFF) << 2, (k >> 8 & 0xFF) << 2, (k & 0xFF) << 2)
}

switch a[2] {
case "color":
    let x = Int(a[3])!, y = Int(a[4])!
    var rs: [Int] = [], gs: [Int] = [], bs: [Int] = []
    for dy in -1...1 { for dx in -1...1 { let c = px(x + dx, y + dy); rs.append(c.0); gs.append(c.1); bs.append(c.2) } }
    let c = (rs.sorted()[4], gs.sorted()[4], bs.sorted()[4]); print(hex(c), String(format: "L=%.0f", lum(c)))
case "mode":
    let c = modeColor(Int(a[3])!, Int(a[4])!, Int(a[5])!, Int(a[6])!); print(hex(c), String(format: "L=%.0f", lum(c)))
case "scan":
    let horiz = a[3] == "h", at = Int(a[4])!, from = Int(a[5])!, to = Int(a[6])!, thr = a.count > 7 ? Double(a[7])! : 12
    var prev = lum(horiz ? px(from, at) : px(at, from)); var out: [String] = []
    for p in (from + 1)...to {
        let c = horiz ? px(p, at) : px(at, p); let l = lum(c)
        if abs(l - prev) > thr { out.append("\(p):\(hex(c))") }
        prev = l
    }
    print(out.joined(separator: " "))
case "ink":
    let x0 = Int(a[3])!, y0 = Int(a[4])!, x1 = Int(a[5])!, y1 = Int(a[6])!, thr = a.count > 7 ? Int(a[7])! : 40
    let bg = modeColor(x0, y0, x1, y1)
    var rowF = [Bool](repeating: false, count: y1 - y0 + 1), colF = [Bool](repeating: false, count: x1 - x0 + 1)
    var minX = Int.max, minY = Int.max, maxX = -1, maxY = -1
    for y in y0...y1 { for x in x0...x1 where dist(px(x, y), bg) > thr {
        rowF[y - y0] = true; colF[x - x0] = true; minX = min(minX, x); maxX = max(maxX, x); minY = min(minY, y); maxY = max(maxY, y) } }
    print("bg \(hex(bg))  bbox x\(minX)-\(maxX) y\(minY)-\(maxY)  (w\(maxX - minX + 1) h\(maxY - minY + 1))")
    print("rows", runs(rowF, offset: y0).map { "\($0.0)-\($0.1)(\($0.1 - $0.0 + 1))" }.joined(separator: " "))
    print("cols", runs(colF, offset: x0, minGap: 6).map { "\($0.0)-\($0.1)" }.joined(separator: " "))
case "peak":
    // the text colour of a region: the pixel furthest from the region's background
    let x0 = Int(a[3])!, y0 = Int(a[4])!, x1 = Int(a[5])!, y1 = Int(a[6])!
    let bg = modeColor(x0, y0, x1, y1); var best = bg; var bd = -1
    for y in y0...y1 { for x in x0...x1 { let c = px(x, y); let d = dist(c, bg); if d > bd { bd = d; best = c } } }
    print("text \(hex(best)) L=\(Int(lum(best)))  on bg \(hex(bg)) L=\(Int(lum(bg)))")
default: print("unknown")
}
