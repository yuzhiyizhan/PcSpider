
function $(e){
    Xt = new Map()
    function aaa(e, t) {
        if (null == e)
            return {};
        var n, r, o = function(e, t) {
            if (null == e)
                return {};
            var n, r, o = {}, i = Object.keys(e);
            for (r = 0; r < i.length; r++)
                n = i[r],
                t.indexOf(n) >= 0 || (o[n] = e[n]);
            return o
        }(e, t);
        if (Object.getOwnPropertySymbols) {
            var i = Object.getOwnPropertySymbols(e);
            for (r = 0; r < i.length; r++)
                n = i[r],
                t.indexOf(n) >= 0 || Object.prototype.propertyIsEnumerable.call(e, n) && (o[n] = e[n])
        }
        return o
    }
    function r(e) {
        if (Array.isArray(e))
            return e
    }
    function o(e) {
        if ("undefined" !== typeof Symbol && null != e[Symbol.iterator] || null != e["@@iterator"])
            return Array.from(e)
    }
    function a(e, t) {
        if (e) {
            if ("string" === typeof e)
                return (0,
                    r.Z)(e, t);
            var n = Object.prototype.toString.call(e).slice(8, -1);
            return "Object" === n && e.constructor && (n = e.constructor.name),
                "Map" === n || "Set" === n ? Array.from(n) : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? (0,
                    r.Z)(e, t) : void 0
        }
    }
    function i() {
        throw new TypeError("Invalid attempt to destructure non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
    }
    function sss(e, t) {
        return (0,
            r)(e) || (0,
            o)(e, t) || (0,
            a)(e, t) || (0,
            i)()
    }
    function automatic1111(e) {
        var t = e.prompt
            , n = e.negativePrompt
            , r = (e.resources,
            aaa(e, ["prompt", "negativePrompt", "resources"]))
            , i = [t];
        n && i.push("Negative prompt: ".concat(n));
        var s = []
            , l = !0
            , c = !1
            , u = void 0;
        try {
            for (var d, f = Object.entries(r)[Symbol.iterator](); !(l = (d = f.next()).done); l = !0) {
                var p, h = (0,
                    sss)(d.value, 2), m = h[0], g = h[1], y = null !== (p = Xt.get(m)) && void 0 !== p ? p : m;
                "hashes" !== y && s.push("".concat(y, ": ").concat(g))
            }
        } catch (v) {
            c = !0,
                u = v
        } finally {
            try {
                l || null == f.return || f.return()
            }
            finally {
                if (c)
                    throw u
            }
        }
        return s.length > 0 && i.push(s.join(", ")),
            i.join("\n")
    }
    return automatic1111(e)
}






