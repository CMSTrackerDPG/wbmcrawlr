#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2018 CERN
#
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from wbmcrawlr import oms
from wbmcrawlr.oms import get_lumisection_count
import pytest


def test_get_run():
    run = oms.get_run(327564)

    runs_fields = [
        "run_number",
        "fill_number",
        "stable_beam",
        "fill_type_runtime",
        "duration",
        "start_time",
        "end_time",
        "delivered_lumi",
        "recorded_lumi",
        "init_lumi",
        "end_lumi",
        "b_field",
        "energy",
        "clock_type",
        "sequence",
        "l1_hlt_mode_stripped",
        "cmssw_version",
        "initial_prescale_index",
        "tier0_transfer",
        "l1_key_stripped",
        "l1_menu",
        "l1_triggers_counter",
        "l1_rate",
        "hlt_key",
        "hlt_physics_size",
        "hlt_physics_rate",
        "hlt_physics_counter",
        "hlt_physics_throughput",
        "components",
    ]

    assert run["id"] == "327564"
    assert run["attributes"]["delivered_lumi"] == 8.117866
    assert run["attributes"]["recorded_lumi"] == 7.763654
    assert run["attributes"]["l1_key"] == "l1_trg_collisionshi2018/v28"

    for field in runs_fields:
        assert field in run["attributes"]


def test_get_runs():
    runs = oms.get_runs(326941, 326942)
    assert len(runs) == 2
    assert runs[0]["run_number"] == 326941
    assert runs[1]["run_number"] == 326942


def test_get_runs_big_range():
    runs = oms.get_runs(326741, 326942)
    assert len(runs) == 117


def test_get_non_existing_runs():
    runs = oms.get_runs(12345678, 12345688)
    assert len(runs) == 0


def test_get_fill():
    fill = oms.get_fill(7492)
    assert fill["id"] == "7492"
    assert fill["attributes"]["fill_number"] == 7492
    assert fill["attributes"]["fill_type_runtime"] == "IONS"
    assert fill["attributes"]["energy"] == 6369
    assert fill["attributes"]["delivered_lumi"] == 8.107441
    assert fill["attributes"]["recorded_lumi"] == 7.753413
    assert fill["attributes"]["crossing_angle"] == 160


def test_get_fill_2():
    fill = oms.get_fill(6477)
    assert fill["id"] == "6477"
    assert fill["attributes"]["fill_number"] == 6477


def test_get_fills():
    fills = oms.get_fills(7480, 7483)
    assert len(fills) == 4
    assert fills[0]["fill_number"] == 7480
    assert fills[1]["fill_number"] == 7481
    assert fills[2]["fill_number"] == 7482
    assert fills[3]["fill_number"] == 7483


def test_get_fills_2():
    fills = oms.get_fills(6477, 6477)
    assert len(fills) == 1


def test_get_fills_big_range():
    fills = oms.get_fills(7000, 7495)
    assert len(fills) == 496


class TestGetLumisections:
    def test_get_lumisections_by_run_number(self):
        lumis = oms.get_lumisections(319579)
        assert len(lumis) == 3259
        assert "lumisection_number" in lumis[0]

    def test_get_lumisections_by_fill_number(self):
        lumis = oms.get_lumisections(fill_number=6919)
        assert len(lumis) == 3754
        assert "lumisection_number" in lumis[0]

    def test_get_lumisections_by_time_range(self):
        lumis = oms.get_lumisections(
            start_time="2016-12-04T11:23:52Z", end_time="2016-12-04T14:57:10Z"
        )
        assert len(lumis) == 549
        assert "lumisection_number" in lumis[0]

@pytest.mark.skip(reason="Takes a very long time")
def test_get_hltpathinfos():
    hltpathinfos = oms.get_hltpathinfos(319579)
    assert len(hltpathinfos) == 665
    path_names = [info["path_name"] for info in hltpathinfos]
    assert "HLT_AK8PFJet400_TrimMass30_v12" in path_names


def test_get_hltpathrates():
    run_number = 319579
    path_name = "HLT_TrkMu16_DoubleTrkMu6NoFiltersNoVtx_v12"
    hltpathrates = oms.get_hltpathrates(run_number, path_name)
    assert 3167 == len(hltpathrates)


def test_get_lumisection_count():
    #assert 37 == get_lumisection_count(327267) # for when cms_active filter works
    assert 45 == get_lumisection_count(327267) # cms_active filter cannot be added anymore



def test_get_fills_split_filling_scheme():
    fills = oms.get_fills(7480, 7483, split_filling_scheme=True)
    assert len(fills) == 4
    assert fills[0]["fill_number"] == 7480
    assert fills[1]["fill_number"] == 7481
    assert fills[2]["fill_number"] == 7482
    assert fills[3]["fill_number"] == 7483

    fill = fills[0]

    assert "injection_scheme" in fill
    assert "injection_scheme_spacing" in fill

    assert fill["injection_scheme"] == '75_150ns_733Pb_733_702_468_42bpi_20inj'
    assert fill["injection_scheme_spacing"] == '75'


def test_get_fill_split_filling_scheme_none_type():
    fill_number = 6000
    fills = oms.get_fills(fill_number, fill_number, split_filling_scheme=True)
    fill = fills[0]
    assert len(fills) == 1
    assert "injection_scheme" in fill
    assert "injection_scheme_spacing" in fill

def test_get_fill_split_filling_scheme_3():
    fill_number = 6082
    fills = oms.get_fills(fill_number, fill_number, split_filling_scheme=True)
    fill = fills[0]
    assert len(fills) == 1
    assert "injection_scheme" in fill
    assert fill["injection_scheme_spacing"] == None
    assert fill["injection_scheme_bunches"] == "25ns"

def test_get_fills_split_filling_scheme_big_range():
    fills = oms.get_fills(6000, 7000, split_filling_scheme=True)
    assert len(fills) > 4
    fill = fills[0]

    assert "injection_scheme" in fill
    assert "injection_scheme_spacing" in fill
