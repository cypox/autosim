set part xc7z020clg484-1
set board em.avnet.com:zed:part0:1.3
set parent /home/cy/dac-2019/autosim/project
set project /home/cy/dac-2019/autosim/project/project.xpr
set top sq_mult
set source_dir /home/cy/dac-2019/autosim/sources

proc create_report { reportName command } {
  set status "."
  append status $reportName ".fail"
  if { [file exists $status] } {
    eval file delete [glob $status]
  }
  send_msg_id runtcl-4 info "Executing : $command"
  set retval [eval catch { $command } msg]
  if { $retval != 0 } {
    set fp [open $status w]
    close $fp
    send_msg_id runtcl-5 warning "$msg"
  }
}

exec rm -rf $parent
exec mkdir $parent
cd $parent

create_project -in_memory -part $part

set_property webtalk.parent_dir $parent [current_project]
set_property parent.project_path $project [current_project]
set_property default_lib xil_defaultlib [current_project]
set_property target_language Vhdl [current_project]
set_property board_part $board [current_project]

foreach file [glob -nocomplain -directory $source_dir *.vhd] {
  file copy $file $parent
  read_vhdl -library xil_defaultlib $file
}

synth_design -top $top -part $part

create_report "synth_utilization" "report_utilization -file utilization_synth.rpt -pb utilization_synth.pb"

opt_design

create_report "impl_drc" "report_drc -file drc_opted.rpt -pb drc_opted.pb -rpx drc_opted.rpx"

place_design

create_report "place_io" "report_io -file io_placed.rpt"
create_report "place_utilization" "report_utilization -file utilization_placed.rpt -pb utilization_placed.pb"
create_report "place_control" "report_control_sets -verbose -file control_sets_placed.rpt"

route_design

create_report "route_drc" "report_drc -file drc_routed.rpt -pb drc_routed.pb -rpx drc_routed.rpx"
create_report "route_methodology" "report_methodology -file methodology_drc_routed.rpt -pb methodology_drc_routed.pb -rpx methodology_drc_routed.rpx"
create_report "route_power" "report_power -file power_routed.rpt -pb power_summary_routed.pb -rpx power_routed.rpx"
create_report "route_route_status" "report_route_status -file route_status.rpt -pb route_status.pb"
create_report "route_timing_summary" "report_timing_summary -max_paths 10 -file timing_summary_routed.rpt -rpx timing_summary_routed.rpx -warn_on_violation "
create_report "route_incremental_reuse" "report_incremental_reuse -file incremental_reuse_routed.rpt"
create_report "route_clock_utilization" "report_clock_utilization -file clock_utilization_routed.rpt"

cd ..
