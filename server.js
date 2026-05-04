const http = require("http");
const fs = require("fs");
const path = require("path");
const dir = "C:/Users/KK/Documents/GitHub/english-words";
const mime = {".html":"text/html;charset=utf-8",".css":"text/css",".js":"application/javascript"};
http.createServer((req, res) => {
  let fp = path.join(dir, req.url==="/" ? "index.html" : req.url.split("?")[0]);
  fs.readFile(fp, (err, data) => {
    if (err) { res.writeHead(404); res.end("Not found"); return; }
    res.writeHead(200, {"Content-Type": mime[path.extname(fp)]; "text/plain", "Cache-Control":"no-cache"});
    res.end(data);
  });
}).listen(8765, () => console.log("OK"));
