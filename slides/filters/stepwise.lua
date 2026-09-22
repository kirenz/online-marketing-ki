-- stepwise.lua: Folien bauen sich schrittweise auf.
--
-- `incremental: true` wirkt nur auf Listen. Die Decks bestehen aber meist aus
-- Absätzen, Karten (.feature), Zeitstrahlen (.timeline-item) und Spalten.
-- Dieser Filter macht daraus Fragmente:
--   * jede Karte und jeder Zeitstrahl-Punkt erscheint einzeln,
--   * ab der zweiten Spalte erscheint jede Spalte einzeln,
--   * auf Textfolien erscheint jeder Absatz ab dem zweiten einzeln.
-- Ausgenommen sind Stage-Folien, Notizen, Quellenangaben und Folien mit
-- der Klasse .all-at-once (für Folien, die als Ganzes stehen sollen).

local STEP_DIVS = { ["feature"] = true, ["timeline-item"] = true }

local function has_class(el, name)
  for _, c in ipairs(el.classes) do
    if c == name then return true end
  end
  return false
end

local function add_fragment(el)
  if not has_class(el, "fragment") then el.classes:insert("fragment") end
  return el
end

local function mark_divs(blocks)
  return blocks:walk({
    Div = function(div)
      for _, c in ipairs(div.classes) do
        if STEP_DIVS[c] then return add_fragment(div) end
      end
      if has_class(div, "columns") then
        local n = 0
        for _, child in ipairs(div.content) do
          if child.t == "Div" and has_class(child, "column") then
            n = n + 1
            if n > 1 then add_fragment(child) end
          end
        end
        return div
      end
    end,
  })
end

function Pandoc(doc)
  if not quarto.doc.is_format("revealjs") then return doc end
  local out = pandoc.List()
  local skip_slide = false
  local paras = 0
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level <= 2 then
      skip_slide = has_class(block, "stage") or has_class(block, "all-at-once")
      paras = 0
      out:insert(block)
    elseif skip_slide then
      out:insert(block)
    elseif block.t == "Para" then
      paras = paras + 1
      if paras > 1 then
        out:insert(pandoc.Div({ block }, pandoc.Attr("", { "fragment" })))
      else
        out:insert(block)
      end
    elseif block.t == "Div" and (has_class(block, "notes") or has_class(block, "sources")) then
      out:insert(block)
    else
      out:insert(mark_divs(pandoc.Blocks({ block }))[1])
    end
  end
  doc.blocks = out
  return doc
end
