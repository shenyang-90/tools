# Scripts/pr/openroad.mk - OpenROAD物理设计模板

OUT_DIR         ?= ../../Temp/OpenROAD
SCRIPTS_DIR     ?= .
RTL_TOP         ?= {{RTL_TOP}}

.PHONY: floorplan place cts route final pr clean

floorplan:
	@mkdir -p $(OUT_DIR)
	@echo "[OpenROAD] Floorplan..."
	openroad -exit $(SCRIPTS_DIR)/floorplan.tcl \
		-log $(OUT_DIR)/floorplan.log

place: floorplan
	@echo "[OpenROAD] Placement..."
	openroad -exit $(SCRIPTS_DIR)/place.tcl \
		-log $(OUT_DIR)/place.log

cts: place
	@echo "[OpenROAD] CTS..."
	openroad -exit $(SCRIPTS_DIR)/cts.tcl \
		-log $(OUT_DIR)/cts.log

route: cts
	@echo "[OpenROAD] Routing..."
	openroad -exit $(SCRIPTS_DIR)/route.tcl \
		-log $(OUT_DIR)/route.log

final: route
	@echo "[OpenROAD] Final..."
	openroad -exit $(SCRIPTS_DIR)/final.tcl \
		-log $(OUT_DIR)/final.log

pr: final
	@echo "[OpenROAD] Physical design complete"
	@echo "Output: $(OUT_DIR)/$(RTL_TOP).gds"

clean:
	@rm -rf $(OUT_DIR)
	@echo "[OpenROAD] Cleaned"
