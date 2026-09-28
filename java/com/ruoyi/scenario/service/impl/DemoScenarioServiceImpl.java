package com.ruoyi.scenario.service.impl;

import java.util.List;
import java.util.Map;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.scenario.mapper.DemoScenarioMapper;
import com.ruoyi.scenario.domain.DemoScenario;
import com.ruoyi.scenario.service.IDemoScenarioService;

/**
 * 云场景Service业务层处理
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
@Service
public class DemoScenarioServiceImpl implements IDemoScenarioService 
{
    @Autowired
    private DemoScenarioMapper demoScenarioMapper;

    /**
     * 查询云场景
     * 
     * @param sceId 云场景主键
     * @return 云场景
     */
    @Override
    public DemoScenario selectDemoScenarioBySceId(Long sceId)
    {
        return demoScenarioMapper.selectDemoScenarioBySceId(sceId);
    }

    /**
     * 查询云场景列表
     * 
     * @param demoScenario 云场景
     * @return 云场景
     */
    @Override
    public List<DemoScenario> selectDemoScenarioList(DemoScenario demoScenario)
    {
        return demoScenarioMapper.selectDemoScenarioList(demoScenario);
    }

    /**
     * 新增云场景
     * 
     * @param demoScenario 云场景
     * @return 结果
     */
    @Override
    public int insertDemoScenario(DemoScenario demoScenario)
    {
        demoScenario.setCreateTime(DateUtils.getNowDate());
        return demoScenarioMapper.insertDemoScenario(demoScenario);
    }

    /**
     * 修改云场景
     * 
     * @param demoScenario 云场景
     * @return 结果
     */
    @Override
    public int updateDemoScenario(DemoScenario demoScenario)
    {
        demoScenario.setUpdateTime(DateUtils.getNowDate());
        return demoScenarioMapper.updateDemoScenario(demoScenario);
    }

    /**
     * 批量删除云场景
     * 
     * @param sceIds 需要删除的云场景主键
     * @return 结果
     */
    @Override
    public int deleteDemoScenarioBySceIds(Long[] sceIds)
    {
        return demoScenarioMapper.deleteDemoScenarioBySceIds(sceIds);
    }

    /**
     * 删除云场景信息
     * 
     * @param sceId 云场景主键
     * @return 结果
     */
    @Override
    public int deleteDemoScenarioBySceId(Long sceId)
    {
        return demoScenarioMapper.deleteDemoScenarioBySceId(sceId);
    }

    /**
     * 提交审核or批量审核通过or单个审核通过和不通过云场景
     *
     * @param params 提交审核or批量审核通过or单个审核通过和不通过的云场景主键ids、审核状态、审核通过时间、审核人、审核不通过原因
     * @return 结果
     */
    @Override
    public int updateScenarioByIds(Map<String, Object> params)
    {
        return demoScenarioMapper.updateScenarioByIds(params);
    }
}
